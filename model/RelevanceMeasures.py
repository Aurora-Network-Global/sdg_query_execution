class RelevanceMeasure:

    def __init__(self):
        self.recall = 0
        self.precision = 0
        self.true_positives = 0
        self.false_negatives = 0
        self.false_positives = 0
        self.number_of_test_entries = 0
        self.total_number_of_query_results = 0
