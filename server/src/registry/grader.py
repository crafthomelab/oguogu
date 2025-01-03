from typing import Dict
from src.domains import Challenge
from src.settings import Settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field   
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
제목: <챌린지 제목>
설명: <어떤 챌린지이며, 어떤 식으로 평가하면 되는지 서술>
기간: <시작일자> ~ <종료일자>

----------
증명 자료는 아래와 같은 포맷으로 제공됩니다.
촬영 일자: <제공된 이미지의 EXIF 데이터 내 촬영 일자, 이미지에 따라 제공되지 않을 수 있음>
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
        
    async def grade_proof(
        self, 
        challenge: Challenge,
        proof_content: Dict[str, any],
    ) -> ProofGraderResponse:
        if challenge.type == "photos":
            return await self.grade_photos_proof(challenge, proof_content)
        else:   
            raise ValueError(f"Unsupported proof type: {challenge.type}"  )

    async def grade_photos_proof(
        self, 
        challenge: Challenge,
        proof_content: Dict[str, any],
    ) -> ProofGraderResponse:
        logger.info(f"Grading proof for challenge {challenge.hash}")
        return await self.chain.ainvoke({
            "title": challenge.title,
            "description": challenge.description,
            "start_date": challenge.start_date.isoformat(),
            "end_date": challenge.end_date.isoformat(),
            "screenshot_date": proof_content["screenshot_date"],
            "image_url": proof_content["image"]
        })
