import json

from brain.memory_engine import memory


class LearningEngine:

    def __init__(self):

        print("Learning Engine Initialized")


    def analyse(self):

        history = memory.load()

        if len(history) == 0:

            return {

                "status":"No history available."

            }

        total = len(history)

        topics = []

        for item in history:

            topics.append(

                item["topic"]

            )

        report = {

            "videos_created": total,

            "recent_topics": topics[-10:]

        }

        return report


    def recommend(self):

        report = self.analyse()

        return {

            "next_action":

            "Create more videos similar to the best performing topics.",

            "report": report

        }


learning = LearningEngine()
