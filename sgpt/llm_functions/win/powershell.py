import subprocess

from instructor import OpenAISchema
from pydantic import Field


class Function(OpenAISchema):
    """
    Executes PowerShell script on Windows and returns the output (result).
    Can be used for actions like: create a file, check for system updates, send an email.
    """

    powershell_script: str = Field(
        ...,
        example='Get-ChildItem C:\\',
        description="PowerShell script to execute.",
    )

    class Config:
        title = "execute_powershell_script"

    @classmethod
    def execute(cls, powershell_script):
        try:
            process = subprocess.Popen(
                ["powershell", powershell_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            output, _ = process.communicate()
            output = output.decode("utf-8").strip()
            return f"Output: {output}"
        except Exception as e:
            return f"Error: {e}"
