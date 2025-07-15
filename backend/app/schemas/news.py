class NewsBase(BaseModel):
    url: HttpUrl
    source: Optional[str]
    title: str
    author: Optional[str]
    published_at: Optional[datetime]
    summary: Optional[str]
    content: Optional[str]
    seeded_at: Optional[datetime]
    bias: Optional[Dict]
    sentiment: Optional[Dict]
    tags: Optional[List[str]]
    enriched_at: Optional[datetime]

class NewsCreate(NewsBase):
    """Schema for incoming news creation"""
    pass

class NewsOut(BaseModel):
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    id: str = Field(alias="_id")
    url: str
    source: Optional[str]
    title: str
    author: Optional[str]
    published_at: Optional[datetime] = None
    summary: Optional[str]
    content: Optional[str]
    seeded_at: Optional[datetime]
    bias: Optional[Dict]
    sentiment: Optional[Dict]
    tags: Optional[List[str]]
    enriched_at: Optional[datetime]

    @classmethod
    def validate(cls, value):
        if isinstance(value, dict) and isinstance(value.get("_id"), object):
            value["_id"] = str(value["_id"])
        return value

    @field_validator("published_at", mode="before")
    @classmethod
    def validate_datetime(cls, v):
        if v in (None, "", "Unknown"):
            return None
        return v
