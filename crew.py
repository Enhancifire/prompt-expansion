import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")


class SceneCrew:

    # Set gemini pro as llm
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        google_api_key=GOOGLE_API_KEY
    )

    # Define Agents
    sceneDetailer = Agent(
        role='Scene Details Inserter',
        goal='Add details to the scene',
        backstory='Experienced in adding details to a sentence, portraying the scene in a vivid manner.',
        allow_delegation=False,
        llm=llm,
    )

    promptWriter = Agent(
        role='Prompt Writer',
        goal='Convert the scene into a text to image model prompt',
        backstory='A seasoned expert in converting sentences into prompts for text to image models.',
        allow_delegation=True,
        llm=llm
    )

    contentSpecialist = Agent(
        role='Content Specialist',
        goal='Critique and refine prompt content',
        backstory='A professional prompt writer with experience in refining content for text to image models.',
        allow_delegation=True,
        llm=llm
    )

    promptManager = Agent(
        role="Flow manager",
        goal="Convert the scene into a text to image model prompt, creating 3 different versions, selecting the best one and returning it.",
        backstory="A seasoned expert in converting sentences into prompts for text to image models.",
        allow_delegation=True,
        llm=llm,
    )

    async def generateScene(self, inp):

        # Define Task
        sceneGenerationTask = Task(
            description=f'''
            1. Add details to the scene provided, portraying the scene in a vivid manner.
            2. Evaluate the written scene for its effectiveness and creativity.
            3. Scrutinize the scene for inconsistencies and clarity.
            4. Adjust the scene to have more details, including lighting, background, texture, and other elements,
            5. Convert the scene into a text to image model prompt.
            6. Return only the generated prompt without anything else.

            Scene: {inp}
            ''',
            agent=self.promptManager
        )

        # Create a Single Crew
        generaterCrew = Crew(
            agents=[
                self.sceneDetailer,
                self.promptWriter,
                self.contentSpecialist,
                self.promptManager
            ],
            tasks=[sceneGenerationTask],
            verbose=True,
            process=Process.sequential
        )

        # Execution Flow
        print("Crew: Working on prompt generation...")
        return generaterCrew.kickoff()

    def saveResult(self, prompt, result):
        with open('results.txt', 'a') as f:
            f.write(f"Scene: {prompt}\n")
            f.write(result)
        print("Result saved to result.txt")
