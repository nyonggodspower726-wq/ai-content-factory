def build(self, topic):

    project = {}

    print("CEO")
    product = recommend_product(topic)
    project["product"] = product

    # CEO Engine
    project["ceo"] = ceo.review(topic, product)

    print("Brand")
    project["brand"] = brand.get_brand()

    print("Trend")
    project["trend"] = discover_trends(topic)

    print("Audience")
    project["audience"] = audience_plan(topic)

    print("Offer")
    project["offer"] = create_offer(
        project["product"],
        project["audience"]
    )

    print("Thinking")
    project["thinking"] = think(
        project["product"],
        topic
    )

    print("Marketing")
    project["marketing"] = marketing_plan(
        project["thinking"]
    )

    print("Psychology")
    project["psychology"] = psychology_plan(
        project["marketing"]
    )

    print("Director")
    project["director"] = create_director_plan(
        project["thinking"]
    )

    print("Storyboard")
    project["storyboard"] = create_storyboard(
        project["director"]
    )

    print("Scene Prompts")
    project["scene_prompts"] = generate_scene_prompts(
        project["storyboard"]
    )

    print("Script")
    project["script"] = generate_script(
        project
    )

    print("Viral Analysis")
    project["viral"] = evaluate_video(
        project["storyboard"]
    )

    print("Decision")
    project["decision"] = final_decision(
        project
    )

    return project
