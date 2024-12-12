phishing_response_schema = {
    "title": "PhishingResponseSchema",
    "description": "A schema representing the structure for classifying email as phishing or clean.",
    "type": "object",
    "properties": {
        "decision": {
            "type": "string",
            "enum": ["Phishing", "Clean"],
            "description": "The decision on whether the email is classified as 'Phishing' or 'Clean'."
        },
        "explanation": {
            "type": "string",
            "description": "A concise explanation justifying the decision."
        }
    },
    "required": ["decision", "explanation"]
}

checker_response_schema = {
    "title": "CheckerResponseSchema",
    "description": "A schema representing the structure for validating a phishing detection agent's response.",
    "type": "object",
    "properties": {
        "validation": {
            "type": "string",
            "enum": ["Repeat", "Valid"],
            "description": "The result of the validation. 'Repeat' if the response is invalid, 'Valid' if the "
                           "response meets the requirements."
        }
    },
    "required": ["validation"]
}
