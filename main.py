def main(self=None):
    print("\nMediBELL – Privacy-Preserving IoT Healthcare System")
    print("1. Train baseline model (No DP)")
    print("2. Train DP model")
    print("3. Evaluate DP model")
    print("4. Run epsilon experiment")
    print("5. Predict disease")
    print("0. Exit")

    choice = input("Select option: ")

    if choice == "1":
        import baseline_fresh
    elif choice == "2":
        import train_dp
    elif choice == "3":
        import evaluate
    elif choice == "4":
        import epsilon_experiment
    elif choice == "5":
        import predict_dp_interactive
    elif choice == "0":
        print("Exiting system.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
