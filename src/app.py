import gradio as gr
from crewai_readme_generator.crew import CrewaiReadmeCreator
import os

def run_crew(folder, language):
    inputs = {
        'folder': folder,
        'language': language
    }
    crew = CrewaiReadmeCreator()
    folder = os.path.abspath(folder)
    crew.set_folder(folder)
    result = crew.crew().kickoff(inputs=inputs)
    return result

def main():
    with gr.Blocks() as app:
        gr.Markdown("# Crewai Readme Creator")
        folder_input = gr.Textbox(label="Folder Path", placeholder="Enter the folder path")
        language_input = gr.Textbox(label="Language", placeholder="Enter the language (e.g., 'en')")
        
        run_button = gr.Button("Run Crew")
        output = gr.Textbox(label="Output", interactive=False)

        run_button.click(run_crew, inputs=[folder_input, language_input], outputs=output)

    app.launch()

if __name__ == "__main__":
    main() 