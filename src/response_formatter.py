class ResponseFormatter:

    @staticmethod
    def format_response(title, body, disclaimer=True):

        response = f"## {title}\n\n{body}"

        if disclaimer:
            response += (
                "\n\n---"
                "\n⚠️ This information is for educational purposes only "
                "and should not replace professional medical advice."
            )

        return response