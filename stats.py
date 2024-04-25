class Stats:
    def __init__(self, num_players):
        self.character_matrix = [[0 for _ in range(8)] for _ in range(num_players)]
        self.special_dict = {}

    def process_averages(self, scores):
        positions = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        self.special_dict = {k: positions[self.special_dict[k]]+1 for k in self.special_dict.keys()}
        averages = [0 for _ in range(8)]
        for i in range(8):
            uses = sum(self.character_matrix[j][i] for j in range(len(scores)))
            if uses == 0:
                averages[i] = (len(scores) + 1) / 2
                continue
            averages[i] = (sum([self.character_matrix[j][i] * (positions[j]+1) for j in range(len(scores))])) / uses
        return averages
