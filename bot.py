from content.trend_finder import get_trending_topic
from content.script_writer import generate_script

def main():
    print("===================================")
    print("     AI CONTENT FACTORY STARTED")
    print("===================================")

    topic = get_trending_topic()
    print(f"Topic: {topic}")

    script = generate_script(topic)
    print("\nGenerated Script:\n")
    print(script)

if __name__ == "__main__":
    main()
