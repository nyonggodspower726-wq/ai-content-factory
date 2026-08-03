from brain.project_memory import project
from brain.monitor import monitor
from brain.recovery_manager import recovery

from brain.trend_engine import discover_trends
from brain.thinking_engine import think
from brain.marketing_engine import marketing_plan
from brain.psychology_engine import psychology_plan
from brain.director import create_director_plan
from brain.storyboard import create_storyboard
from brain.product_engine import recommend_product
from brain.script_engine import generate_script
from brain.seo_engine import generate_seo
from brain.voice_engine import generate_voice
from brain.quality_engine import quality_check
from brain.optimizer_engine import optimize


class MasterAI:

    def execute(self, topic):

        project.clear()

        monitor.start("Trend Engine")
        trend = recovery.execute(discover_trends, topic)
        project.set("trend", trend)
        monitor.finish()

        monitor.start("Thinking Engine")
        thinking = recovery.execute(think, topic)
        project.set("thinking", thinking)
        monitor.finish()

        monitor.start("Marketing Engine")
        marketing = recovery.execute(marketing_plan, topic)
        project.set("marketing", marketing)
        monitor.finish()

        monitor.start("Psychology Engine")
        psychology = recovery.execute(psychology_plan, marketing)
        project.set("psychology", psychology)
        monitor.finish()

        monitor.start("Director Engine")
        director = recovery.execute(create_director_plan, topic)
        project.set("director", director)
        monitor.finish()

        monitor.start("Storyboard Engine")
        storyboard = recovery.execute(create_storyboard, director)
        project.set("storyboard", storyboard)
        monitor.finish()

        monitor.start("Product Engine")
        product = recovery.execute(recommend_product, topic)
        project.set("product", product)
        monitor.finish()

        monitor.start("Script Engine")
        script = recovery.execute(generate_script, project.export())
        project.set("script", script)
        monitor.finish()

        monitor.start("SEO Engine")
        seo = recovery.execute(generate_seo, topic)
        project.set("seo", seo)
        monitor.finish()

        monitor.start("Voice Engine")
        voice = recovery.execute(generate_voice, project.export())
        project.set("voice", voice)
        monitor.finish()

        monitor.start("Quality Engine")
        quality = recovery.execute(quality_check, project.export())
        project.set("quality", quality)
        monitor.finish()

        monitor.start("Optimizer Engine")
        optimized = recovery.execute(optimize, project.export())
        project.set("optimized", optimized)
        monitor.finish()

        monitor.summary()

        return project.export()


master_ai = MasterAI()
