
import base64
from io import BytesIO
from typing import Dict, Optional
from src.domains import Challenge
from src.settings import Settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field   
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ProofGraderResponse(BaseModel):
    is_correct: bool = Field(
        description="제출한 자료가 챌린지 조건을 만족하는지 여부"
    )
    
    message: str = Field(
        description="제출한 자료가 챌린지 조건을 만족하지 않을 경우,"
                    "왜 만족하지 않았는지 설명."
                    "제출한 자료가 챌린지 조건을 만족할 경우,"
                    "한 줄로 챌린지 조건을 통과했음을 축하하는 메시지를 반환"
    )
    
    
SYSTEM_PROMPT = """당신은 사용자가 챌린지를 수행했는지를 확인하는 검증자입니다.
사용자는 챌린지의 제목과 설명을 제출하고, 챌린지 조건을 만족하는 증명 자료를 사진으로 제출합니다.
증명 자료는 어플리케이션의 화면에 대한 스크린샷이나, 유저가 챌린지를 수행하는 모습을 촬영한 사진 등으로 구성됩니다.
당신은 제공받은 증명 자료가 챌린지 조건을 만족하는지 확인해야 합니다.

유저가 제출한 증명 자료가 챌린지에 부합하지 않은 경우가 발생할 수 있으며, 다음과 같은 이유로 부합하지 않을 수 있습니다.
- 사진 속 내용이 챌린지 내용과 다른 경우
- 증명 자료가 챌린지 기간 내에 진행된 것이 아닌 것으로 보이는 경우
- 증명 자료의 내용이 명백히 타인의 것으로 보이는 경우

당신은 챌린지 조건을 만족하는 증명 자료일 경우, 챌린지 조건을 통과했음을 축하하는 메시지를 반환해야 합니다.
당신은 챌린지 조건을 만족하지 않는 증명 자료일 경우, 왜 만족하지 않았는지 설명해야 합니다.

챌린지 정보는 아래와 같은 포맷으로 제공됩니다.
제목: 
설명: 
기간: 
----------
증명 자료는 아래와 같은 포맷으로 제공됩니다.
촬영 일자: 
"""

class ProofGrader:
    def __init__(self, settings: Settings):
        self.settings = settings
        
        model = ChatOpenAI(
            model_name=settings.OPENAI_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.OPENAI_MODEL_TEMPERATURE
        )
        
        model = model.with_structured_output(ProofGraderResponse)
        prompt = ChatPromptTemplate(messages=[
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(
                [
                    {
                        "type": "text", 
                        "text": 
                            "챌린지 정보\n"
                            "제목: {title}\n"
                            "설명: {description}\n"
                            "기간: {start_date} ~ {end_date}\n"
                            "----------\n"
                            "증명 자료\n"
                            "촬영 일자: {screenshot_date}\n"
                    }, 
                    {"type": "image_url", "image_url": {"url": "{image_url}"}}
                ]
            )
        ], input_variables=["title", "description", "image_url"])
        
        self.chain = prompt | model
        
    def grade_proof(
        self, 
        challenge: Challenge,
        proof_content: Dict[str, any],
    ) -> ProofGraderResponse:
        if challenge.type == "photos":
            return self.grade_photos_proof(challenge, proof_content)
        else:   
            raise ValueError(f"Unsupported proof type: {challenge.type}"  )

    async def grade_photos_proof(
        self, 
        challenge: Challenge,
        proof_content: Dict[str, any],
    ) -> ProofGraderResponse:
        logger.info(f"Grading proof for challenge {challenge.hash}")
        content_type = proof_content["content_type"]
        image_bytes = proof_content["image_bytes"]
        
        screenshot_date = extract_screenshot_date(image_bytes) 
        return await self.chain.ainvoke({
            "title": challenge.title,
            "description": challenge.description,
            "start_date": challenge.start_date.isoformat(),
            "end_date": challenge.end_date.isoformat(),
            "screenshot_date": screenshot_date,
            "image_url": encode_image_url(content_type, image_bytes)
        })
        
        
def encode_image_url(
    content_type: str,
    image_bytes: bytes
):
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:{content_type};base64,{base64_image}"

def extract_screenshot_date(
    image_bytes: bytes
) -> Optional[str]:
    image = Image.open(BytesIO(image_bytes))
    exif_data = image._getexif()
    
    if exif_data is not None:
        # 촬영 시각 가져오기 (EXIF 태그 36867: DateTimeOriginal)
        return exif_data.get(36867)