from brain.memory_engine import memory


class LearningEngine:

    def __init__(self):

        print("Learning Engine Initialized")


    def analyse(self):

        history = memory.load()

        if not history:

            return {
                "status": "No history available."
            }

        total = len(history)

        topics = []
        approved = 0
        rejected = 0

        for item in history:

            topics.append(item.get("topic", ""))

            decision = item.get("decision", {})

            if isinstance(decision, dict):

                if decision.get("produce"):

                    approved += 1

                else:

                    rejected += 1

        report = {

            "videos_created": total,

            "approved_projects": approved,

            "rejected_projects": rejected,

            "approval_rate": round(
                (approved / total) * 100,
                2
            ),

            "recent_topics": topics[-10:]

        }

        return report


    def recommend(self):

        report = self.analyse()

        recommendations = []

        if report.get("videos_created", 0) < 10:

            recommendations.append(
                "Produce more videos to improve learning."
            )

        if report.get("approval_rate", 0) < 80:

            recommendations.append(
                "Improve hooks, storytelling and marketing strategy."
            )

        if not recommendations:

            recommendations.append(
                "Current production quality is good. Continue producing similar content."
            )

        return {

            "next_action": recommendations,

            "report": report

        }


    def learn(self, project):

        print("=" * 60)
        print("Learning from latest production...")
        print("=" * 60)

        return self.recommend()


learning = LearningEngine()
