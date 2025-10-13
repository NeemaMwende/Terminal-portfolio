import {
    parse_pdf,
    extract_sections,
    format_response,
    answer_question
} from "jac.lib";

node resume {
    has sections: dict;
    has full_text: str;
}

edge connects {
    has confidence: float;
}

walker parse_resume {
    has file_path: str;
    
    can parse_file;
    can extract_all_sections;
    can format_output;
    
    parse_file -> extract_all_sections;
    
    parse_file {
        print("Parsing resume from:", file_path);
        "Read PDF file and extract text";
    }
    
    extract_all_sections {
        print("Extracting resume sections...");
        "Extract professional summary, skills, experience, etc.";
    }
    
    format_output {
        print("Formatting response for terminal display");
    }
}

walker answer_from_resume {
    has question: str;
    has resume_data: dict;
    
    can search_section;
    can generate_answer;
    
    search_section -> generate_answer;
    
    search_section {
        print("Searching resume for:", question);
        "Match question to relevant resume section";
    }
    
    generate_answer {
        answer = resume_data.get(question, "Not found");
        print("Generated answer:", answer);
    }
}

walker process_command {
    has command: str;
    has resume: resume;
    
    can get_section;
    can format_terminal_output;
    
    get_section {
        section_data = resume.sections.get(command);
        print("Retrieved section:", command);
    }
    
    format_terminal_output {
        formatted = [];
        for line in section_data.split("\n") {
            if line.strip() {
                formatted.append("  • " + line.strip());
            }
        }
        print("\n".join(formatted));
    }
}