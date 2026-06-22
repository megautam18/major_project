import schema
from engine import classifier, matcher, normalizer, scorer
def gateway(text):
    normalizer_op = normalizer.normalize(text)
    matcher_op = matcher.match(normalizer_op)
    scorer_op = scorer.score(matcher_op)
    classifier_op = classifier.classify(scorer_op)
    output_dict = schema.shape_output(
        original=text,
        normalized=normalizer_op,
        matches=matcher_op,
        score=scorer_op,
        verdict=classifier_op
    ) 
    return output_dict

x=gateway("wassup gang")
print(x)
