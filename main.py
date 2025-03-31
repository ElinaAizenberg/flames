import time
import cv2
import pygame
from const import Gesture, FPS
from effects.flames import Flame
from effects.lighting import apply_darkness_with_lights
from effects.smoke import Smoke

from detection import HandDetection, FaceDetection



def main():
    gesture_classifier_model = "hand_detection/model.pkl"
    gesture_classifier_scaler = "hand_detection/scaler.pkl"
    face_classifier_model = "face_detection/model.pkl"
    face_classifier_scaler = "face_detection/scaler.pkl"

    hands_detector = HandDetection(gesture_classifier_model, gesture_classifier_scaler)
    face_detector = FaceDetection(face_classifier_model, face_classifier_scaler)

    pygame.init()
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)

    pygame.display.set_caption("Flame Simulation")

    clock = pygame.time.Clock()
    flame = Flame(40)
    smoke_image = pygame.image.load('effects/smoke.png').convert_alpha()

    smoke = Smoke(smoke_image)

    prev_time = time.time()
    cap = cv2.VideoCapture(0)

    face_mode = True
    main_light_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time

        screen.fill((0, 0, 0))
        overlay.fill((0, 0, 0, 0))

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        if face_mode:
            face_landmarks = face_detector.detect(frame)
            if face_landmarks:
                flame.update_flame(-3)
                normalized_face_landmarks = face_detector.pre_process_landmark(face_landmarks)
                if face_detector.define_face_expression(normalized_face_landmarks):
                    face_mode = False

        else:
            hands_landmarks = hands_detector.detect(frame)
            if hands_landmarks:
                normalized_landmarks = hands_detector.pre_process_landmark(hands_landmarks)
                hand_gesture = hands_detector.define_gesture(normalized_landmarks)

                pointer_finger = hands_landmarks[8]
                flame.x, flame.y = pointer_finger[0], pointer_finger[1]
                main_light_pos = (pointer_finger[0], pointer_finger[1])
                flame.update_flame(1)

                if hand_gesture == Gesture.CLOSE:
                    face_mode = True
                    flame.update_flame(-10)
                    smoke.x, smoke.y = pointer_finger[0], pointer_finger[1]
                    smoke.renew()
            else:
                flame.update_flame(-4)

        if not flame.flame_particles:
            main_light_pos = None

        processed = apply_darkness_with_lights(
            image=frame,
            secondary_lights=flame.flame_particles,
            main_light_pos=main_light_pos,
            main_light_intensity=len(flame.flame_particles),
            base_darkness=0.2
        )

        flame.draw_flame(overlay, dt)
        smoke.update()
        smoke.draw(overlay)

        frame_surface = pygame.image.frombuffer(
            processed.tobytes(),
            processed.shape[1::-1],
            "BGR"
        )

        screen.blit(frame_surface, (0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()




if __name__ == '__main__':
    main()