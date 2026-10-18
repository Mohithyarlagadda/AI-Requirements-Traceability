
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEPENDENCY_CUES = [
    "depends on",
    "requires",
    "only if",
    "must first",
    "before",
    "after",
    "provided that"
]


def classify_relationship(statement_a, statement_b):
    """Classify two statements using a simple text-similarity baseline."""

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([statement_a, statement_b])

    similarity = cosine_similarity(
        vectors[0:1], vectors[1:2]
    )[0][0]

    # Check for identical statements first.
    if statement_a.strip().lower() == statement_b.strip().lower():
        label = "Related"
        explanation = "Both statements contain identical text."

    else:
        combined_text = (
            statement_a + " " + statement_b
        ).lower()

        has_dependency_cue = any(
            cue in combined_text for cue in DEPENDENCY_CUES
        )

        if has_dependency_cue and similarity >= 0.10:
            label = "Direct Dependency"
            explanation = (
                "Dependency-related wording was found, "
                "and the statements share some text."
            )

        elif similarity >= 0.20:
            label = "Related"
            explanation = (
                "The statements have overlapping terms "
                "and high lexical similarity."
            )

        else:
            label = "Unrelated"
            explanation = (
                "The statements have low lexical similarity."
            )

    return {
        "statement_a": statement_a,
        "statement_b": statement_b,
        "relationship": label,
        "similarity": round(float(similarity), 3),
        "explanation": explanation
    }


if __name__ == "__main__":
    first = "The system shall record user login attempts."
    second = "The system shall record all user login attempts."

    result = classify_relationship(first, second)

    print("Relationship:", result["relationship"])
    print("Similarity:", result["similarity"])
    print("Explanation:", result["explanation"])
