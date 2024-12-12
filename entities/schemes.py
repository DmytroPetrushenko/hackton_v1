result_extraction_scheme = {
    "title": "result_extraction_scheme",
    "description": "A scheme representing the structure for extracting all security testing result.",
    "type": "object",
    "properties": {
        RESULT_FIELD: {
            "type": "string",
            "description": "All results of the security testing process."
        }
    },
    "required": [RESULT_FIELD]
}