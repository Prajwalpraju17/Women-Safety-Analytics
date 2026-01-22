import re
from typing import Dict, List

class ThreatDetector:
    def __init__(self):
        self.threat_patterns = [
            r'\b(help|emergency|danger|unsafe|scared|threatened)\b',
            r'\b(following|stalking|harassing)\b',
            r'\b(alone|isolated|trapped)\b'
        ]
        
    def analyze_text(self, text: str) -> Dict:
        
        threat_score = 0
        detected_threats = []
        
        for pattern in self.threat_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                threat_score += len(matches)
                detected_threats.extend(matches)
        
        return {
            'threat_score': min(threat_score, 10),
            'is_threat': threat_score > 0,
            'detected_keywords': detected_threats,
            'confidence': min(threat_score * 0.2, 1.0)
        }
    
    def analyze_voice(self, audio_data) -> Dict:
        # Placeholder for voice analysis
        return {'voice_threat_detected': False, 'stress_level': 0}
    
    def analyze_image(self, image_data) -> Dict:
        # Placeholder for image analysis
        return {'visual_threat_detected': False, 'unsafe_environment': False}