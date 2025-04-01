import discord
from discord.ext import commands
from discord.ui import Button, View
import requests
import PyPDF2
import os 
from docx import Document
import google.generativeai as genai

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='/', intents=intents)


answers = {}

@bot.command()
async def sot(ctx):
    pdf_button = Button(label="PDF", style=discord.ButtonStyle.primary, custom_id="choose_pdf")
    word_button = Button(label="Word", style=discord.ButtonStyle.primary, custom_id="choose_word")

    view = View()
    view.add_item(pdf_button)
    view.add_item(word_button)

    await ctx.send("Chọn định dạng file:", view=view)

    selected_count = 3

    async def button_callback(interaction):
        selected_format = interaction.data['custom_id']
        if selected_format == 'choose_pdf':
            await interaction.response.send_message("Hãy gửi file PDF của bạn.")
        elif selected_format == 'choose_word':
            await interaction.response.send_message("Hãy gửi file Word của bạn.")

        def check(m):
            return m.author == interaction.user and m.attachments

        msg = await bot.wait_for('message', check=check)
        attachment = msg.attachments[0]

        if selected_format == 'choose_pdf' and attachment.filename.endswith('.pdf'):
            await msg.channel.send(f"Đã nhận file PDF: {attachment.filename}")
        elif selected_format == 'choose_word' and (attachment.filename.endswith('.docx') or attachment.filename.endswith('.doc')):
            await msg.channel.send(f"Đã nhận file Word: {attachment.filename}")
        else:
            await msg.channel.send("Định dạng file không đúng. Vui lòng gửi lại file phù hợp.")
            return

        await msg.channel.send("Nhập số lượng câu hỏi bạn muốn:")

        def check_count(m):
            return m.author == interaction.user and m.content.isdigit()

        count_msg = await bot.wait_for('message', check=check_count)
        selected_count = int(count_msg.content)

        file_url = attachment.url
        file_data = requests.get(file_url).content
        with open(attachment.filename, 'wb') as f:
            f.write(file_data)

        await msg.channel.send("Đang xử lý nội dung file, vui lòng chờ...")

        extracted_text = ""
        if selected_format == 'choose_pdf':
            with open(attachment.filename, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted_text += page.extract_text() or ""
        elif selected_format == 'choose_word':
            doc = Document(attachment.filename)
            for para in doc.paragraphs:
                extracted_text += para.text + "\n"

        # 
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Tạo {selected_count} câu hỏi trắc nghiệm từ nội dung sau và chỉ rõ đáp án đúng với định dạng:\nCâu [số]: [Nội dung]\nA. [Đáp án A]\nB. [Đáp án B]\nC. [Đáp án C]\nD. [Đáp án D]\nĐáp án đúng: [A/B/C/D]\n\nNội dung:\n{extracted_text}"
        response = model.generate_content(prompt)

        questions = response.text.strip().split('\n\n')

        for i, question in enumerate(questions):
            parts = question.strip().split('\n')
            question_text = '\n'.join(parts[:-1])
            correct_answer_line = parts[-1]

            if "Đáp án đúng:" in correct_answer_line:
                correct_answer = correct_answer_line.split(":")[-1].strip()
                answers[f"Câu {i+1}"] = correct_answer

            msg = await interaction.channel.send(f"{question_text}")

            reactions = ['🇦', '🇧', '🇨', '🇩']
            for reaction in reactions:
                await msg.add_reaction(reaction)

    pdf_button.callback = button_callback
    word_button.callback = button_callback

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    message = reaction.message
    reactions_map = {'🇦': 'A', '🇧': 'B', '🇨': 'C', '🇩': 'D'}

    if reaction.emoji in reactions_map:
        question_lines = message.content.split('\n')
        if question_lines:
            question_key = question_lines[0].split(':')[0]

            if question_key in answers:
                correct_answer = answers[question_key]
                user_choice = reactions_map[reaction.emoji]

                if user_choice == correct_answer:
                    await message.channel.send(f"✅ Đúng rồi, {user.mention}! Giỏi lắm.")
                else:
                    await message.channel.send(f"❌ Sai rồi, {user.mention}. Đáp án đúng là: {correct_answer}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

bot.run(DISCORD_BOT_TOKEN)
