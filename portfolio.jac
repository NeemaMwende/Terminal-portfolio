import {
    LLM,
    Model
} from "byllm.llm";

glob llm = Model(model_name="gemini/gemini-2.5-flash");

node Portfolio {
    has name: str = "Neema";
    has title: str = "Software Engineer";
    has resume_data: dict;
}

walker PortfolioTerminal {
    has prompt: str;
    has command: str;
    has portfolio: Portfolio;
    
    can extract_resume_info by llm();
    can answer_user_query by llm();
    can format_for_terminal by llm();
    
    extract_resume_info(section: str) -> str {
        """
        Extract specific section from resume PDF.
        Reads the provided resume.pdf file and extracts the requested section
        like professional summary, skills, experience, education, etc.
        """
        prompt = f"""
        Read the resume file and extract the '{section}' section.
        Format it as bullet points suitable for a terminal display.
        Return only the content without headers.
        """;
        return llm(prompt);
    }
    
    answer_user_query(question: str, context: str) -> str {
        """
        Answer user questions based on resume context.
        """
        prompt = f"""
        Based on this resume context:
        {context}
        
        Answer this question: {question}
        Format as bullet points for terminal display.
        """;
        return llm(prompt);
    }
    
    format_for_terminal(content: str) -> str {
        """
        Format response content for terminal display with proper bullets.
        """
        prompt = f"""
        Format this content as bullet points for terminal display:
        {content}
        
        Each point should start with a bullet (•) and be on a new line.
        Keep it concise and professional.
        """;
        return llm(prompt);
    }
}

with entry {
    print("Portfolio Terminal Initialized");
    print("Resume: Neema.pdf loaded");
    print("Type 'help' for available commands");
}s