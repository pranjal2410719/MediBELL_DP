def validate_symptoms(symptoms, expected_len):
    if not isinstance(symptoms, list):
        raise ValueError("Symptoms must be a list")

    if len(symptoms) != expected_len:
        raise ValueError(
            f"Expected {expected_len} symptoms, got {len(symptoms)}"
        )

    for s in symptoms:
        if s not in [0, 1]:
            raise ValueError(
                "Symptoms must be binary (0 or 1)"
            )

    return True
