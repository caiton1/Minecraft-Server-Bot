def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "hey there!"
    if p_message == "test":
        return ":sunglasses:"
    if p_message == "sbeve is back":
        return "https://tenor.com/view/gigachad-minecraft-meme-steve-minecraft-steve-gif-23317593"