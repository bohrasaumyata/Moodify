class MoodDetector:
    def __init__(self):
        # Mood mapping: each mood points to a list of keywords
        self.mood_keywords = {
            'happy': [
                'happy', 'joyful', 'pleased', 'cheerful', 'delighted', 'content', 'elated', 'excited', 'smiling', 'grateful', 'upbeat', 'glad', 'euphoric', 'blissful'
            ],
            'sad': [
                'sad', 'down', 'gloomy', 'depressed', 'unhappy', 'melancholy', 'blue', 'cry', 'miserable', 'tearful', 'disappointed', 'heartbroken'
            ],
            'energetic': [
                'energetic', 'active', 'motivated', 'enthusiastic', 'vibrant', 'lively', 'restless', 'bouncy', 'powerful', 'vigorous', 'charged', 'pumped', 'hyped'
            ],
            'relaxed': [
                'relaxed', 'calm', 'peaceful', 'serene', 'chilled', 'mellow', 'easygoing', 'laid-back', 'soothing', 'tranquil', 'composed', 'restful'
            ],
            'angry': [
                'angry', 'mad', 'furious', 'annoyed', 'irritated', 'upset', 'enraged', 'frustrated', 'outraged', 'bitter', 'cross', 'fuming'
            ],
            'love': [
                'love', 'romantic', 'affectionate', 'caring', 'warm', 'devoted', 'passionate', 'fond', 'adoring', 'amorous'
            ]
        }

    def detect(self, user_input):
        user_input = user_input.lower()
        for mood, keywords in self.mood_keywords.items():
            for word in keywords:
                if word in user_input:
                    return mood
        return 'relaxed'  # Default mood if nothing matches
