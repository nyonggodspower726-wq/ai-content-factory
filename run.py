from bot import main

def run():
    print("=" * 50)
    print("STARTING AI CONTENT FACTORY")
    print("=" * 50)

    try:
        main()
        print("SUCCESS: Content generation completed.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    run()
