import numpy as np

from effects.flames import FlameParticle


def apply_darkness_with_lights(image, secondary_lights: list[FlameParticle], main_light_pos=None, main_light_intensity: int = 1, base_darkness=0.1):
    img = image.astype(np.float32) / 255

    darkened = img * base_darkness

    if main_light_pos:
        y, x = np.indices(img.shape[:2])
        dist_main = np.sqrt((x - main_light_pos[0]) ** 2 + (y - main_light_pos[1]) ** 2)
        main_strength = np.exp(-dist_main / ((main_light_intensity+1)*3))
        secondary_effect = np.zeros_like(img)

        if secondary_lights:
            sorted_particles = sorted(secondary_lights, key=lambda p: p.y)
            selected_particles = []

            y_threshold = image.shape[0] // 15
            last_y = -y_threshold

            for p in sorted_particles:
                if abs(p.y - last_y) >= y_threshold and len(selected_particles) < 7:
                    selected_particles.append(p)
                    last_y = p.y


            for light in selected_particles:
                intensity = 0.2
                dist = np.sqrt((x - light.x) ** 2 + (y - light.y) ** 2)
                strength = intensity * np.exp(-dist / 10)  # Sharper falloff

                secondary_effect[:, :, 0] += strength * 0.1  # B
                secondary_effect[:, :, 1] += strength * 0.6  # G
                secondary_effect[:, :, 2] += strength * 0.8  # R

        lighted_img = darkened + main_strength[..., np.newaxis] * img + secondary_effect
        return np.clip(lighted_img * 255, 0, 255).astype(np.uint8)

    else:
        return np.clip(darkened * 255, 0, 255).astype(np.uint8)
