from fastapi import APIRouter, HTTPException
from .schemas import NerRequest, NerResponse
# from ..models.predictor import NERPredictor
from .schemas import NerEntity
from loguru import logger

# ner_predictor = NERPredictor()
router = APIRouter()


def rule_based_ner(text: str):
    """
    基于规则的简单实体识别
    
    规则示例:
    - 识别日期格式: 2023-01-01
    - 识别电话号码: 13800138000
    - 识别邮箱: example@example.com
    """
    entities = []
    
    # 日期识别
    import re
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    for match in re.finditer(date_pattern, text):
        entities.append({
            "type": "DATE",
            "text": match.group(),
            "start": match.start(),
            "end": match.end(),
            "confidence": 1.0
        })
    
    # 可以添加更多规则...
    
    return entities


# @router.post("/predict", response_model=NerResponse, summary="NER预测")
# async def ner_prediction(request: NerRequest) -> NerResponse:
#     """
#     命名实体识别接口

#     - **text**: 输入文本（必需）
#     - **threshold**: 置信度阈值（可选，默认0.5）
#     """
#     logger.info(f"Received NER request for text: '{request.text[:50]}...'")
#     try:
#         entities = ner_predictor.predict(
#             text=request.text,
#             threshold=request.threshold if request.threshold is not None else 0.5
#         )
#         ner_entities = [NerEntity(**entity) for entity in entities]
#         logger.info(f"Prediction successful, found {len(ner_entities)} entities.")
#         return NerResponse(entities=ner_entities)
#     except Exception as e:
#         logger.error(f"Unhandled exception during NER prediction: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail="Internal server error during NER prediction.")


@router.post("/predict", response_model=NerResponse, summary="基于规则的NER预测")
async def rule_based_ner_prediction(request: NerRequest) -> NerResponse:
    """
    基于规则的命名实体识别接口
    
    - **text**: 输入文本（必需）
    """
    logger.info(f"Received rule-based NER request for text: '{request.text[:50]}...'")
    try:
        entities = rule_based_ner(request.text)
        ner_entities = [NerEntity(**entity) for entity in entities]
        logger.info(f"Rule-based prediction successful, found {len(ner_entities)} entities.")
        return NerResponse(entities=ner_entities)
    except Exception as e:
        logger.error(f"Unhandled exception during rule-based NER prediction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during rule-based NER prediction.")
