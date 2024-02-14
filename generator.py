import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("GPT_BACKEND"),
)


def generate(user_data):

    system_msg = user_data['system']
    messages = user_data['messages']

    messages_list = []

    if system_msg:
        messages_list.append({
            'role': 'system',
            'content': system_msg
        })

    for m in messages:
        if m[0] == 'u':
            messages_list.append({
                'role': 'user',
                'content': m[1]
            })
        elif m[0] == 'ai':
            messages_list.append({
                'role': 'assistant',
                'content': m[1]
            })

    chat_completion = client.chat.completions.create(
        messages=messages_list,
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content


def test():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(chat_completion.choices[0].message.content)
    print(chat_completion)


if __name__ == '__main__':
    test()
