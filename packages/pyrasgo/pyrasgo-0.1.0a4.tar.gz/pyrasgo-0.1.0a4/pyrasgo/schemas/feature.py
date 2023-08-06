from pydantic import BaseModel, Field
from typing import List, Optional

from pyrasgo.schemas.attributes import Attribute
from pyrasgo.schemas.granularity import Granularity
from pyrasgo.schemas.feature_set import BasicFeatureSet


class FeatureBase(BaseModel):
    id: int


class FeatureCreate(BaseModel):
    name: str
    code: Optional[str]
    description: Optional[str]
    columnId: int
    featureSetId: Optional[int]
    orchestrationStatus: Optional[str]
    tags: Optional[List[str]]
    gitRepo: Optional[str]

class FeatureUpdate(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    gitRepo: Optional[str]
    #Can't include these until we create a v1 patch endpoint for features
    #columnId: Optional[int]
    #featureSetId: Optional[int]
    #organizationId: Optional[int]
    orchestrationStatus: Optional[str]
    #tags: Optional[List[str]]

class Feature(FeatureBase):
    id: str  # TODO: Returning feature ids as strings, ensure consistency.
    name: str = Field(alias="displayName")
    description: Optional[str]
    code: Optional[str] = Field(alias="columnName")
    columnId: Optional[int]
    dataType: Optional[str]
    featureSet: Optional[BasicFeatureSet]
    granularities: Optional[List[Granularity]]
    orchestrationStatus: Optional[str] = Field(alias="status")
    tags: Optional[List[str]]
    attributes: Optional[List[Attribute]]
    gitRepo: Optional[str]
    organizationId: Optional[int]
    class Config:
        allow_population_by_field_name = True

class FeatureStats(BaseModel):
    recCt: Optional[int]
    distinctCt: Optional[int]
    nullRecCt: Optional[int]
    zeroValRecCt: Optional[int]
    meanVal: Optional[str]
    medianVal: Optional[str]
    maxVal: Optional[str]
    minVal: Optional[str]
    sumVal: Optional[str]
    stdDevVal: Optional[str]
    varianceVal: Optional[str]
    rangeVal: Optional[str]
    skewVal: Optional[str]
    kurtosisVal: Optional[str]
    q1Val: Optional[str]
    q3Val: Optional[str]
    IQRVal: Optional[str]
    pct5Val: Optional[str]
    pct95Val: Optional[str]
    outlierCt: Optional[str]
    lowOutlier: Optional[str]
    highOutlier: Optional[str]