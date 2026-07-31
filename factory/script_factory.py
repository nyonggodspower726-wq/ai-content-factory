from brain.script_engine import generate_script


class ScriptFactory:

    def __init__(self):
        print("Script Factory Ready")

    def create(self, topic):

        print("Generating Script...")

        script = generate_script(topic)

        return {
            "topic": topic,
            "script": script
        }


script_factory = ScriptFactory()
