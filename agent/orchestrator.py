"""
Learning Engine - The Heart of Self-Improvement
Analyzes every video, learns from patterns, improves next video
"""

from datetime import datetime
from agent.database import db
from agent.logger import setup_logger

logger = setup_logger(__name__)

class LearningEngine:
    """Analyzes video performance and learns"""
    
    def __init__(self):
        self.patterns = {}
    
    def analyze_video_performance(self, youtube_id: str, metrics: dict):
        """
        Analyze video metrics and extract learnings
        
        metrics = {
            'views': 150,
            'ctr': 6.2,  # click-through rate
            'watch_time_avg': 8.34,
            'watch_time_target': 12.00,
            'watch_percentage': 69.5,
            'comments': 12,
            'shares': 3,
            'affiliate_clicks': 7
        }
        """
        logger.info(f"Analyzing video: {youtube_id}")
        
        learnings = {
            'timestamp': datetime.now().isoformat(),
            'video_id': youtube_id,
            'metrics': metrics,
            'insights': []
        }
        
        # CTR Analysis (Target: 5%+)
        ctr = metrics.get('ctr', 0)
        if ctr >= 5:
            learnings['insights'].append({
                'type': 'thumbnail_success',
                'message': f"CTR {ctr}% - Thumbnail formula working!",
                'pattern': 'thumbnail_bold_number',
                'success': True
            })
        else:
            learnings['insights'].append({
                'type': 'thumbnail_warning',
                'message': f"CTR low at {ctr}% - Need better thumbnail",
                'pattern': 'thumbnail_needs_improvement',
                'success': False
            })
        
        # Watch Time Analysis (Target: 65%+)
        watch_pct = metrics.get('watch_percentage', 0)
        if watch_pct >= 65:
            learnings['insights'].append({
                'type': 'script_success',
                'message': f"Watch time {watch_pct}% - Script engaging!",
                'pattern': 'script_pacing_good',
                'success': True
            })
        else:
            learnings['insights'].append({
                'type': 'script_warning',
                'message': f"Watch time {watch_pct}% - Script too slow/boring",
                'pattern': 'script_needs_improvement',
                'success': False
            })
        
        # Engagement Analysis
        comments = metrics.get('comments', 0)
        if comments >= 30:
            learnings['insights'].append({
                'type': 'engagement_success',
                'message': f"High engagement: {comments} comments!",
                'pattern': 'cta_strong',
                'success': True
            })
        else:
            learnings['insights'].append({
                'type': 'engagement_warning',
                'message': f"Low engagement: {comments} comments - Weak CTA",
                'pattern': 'cta_needs_improvement',
                'success': False
            })
        
        # Affiliate Analysis
        affiliate_clicks = metrics.get('affiliate_clicks', 0)
        if affiliate_clicks >= 20:
            learnings['insights'].append({
                'type': 'affiliate_success',
                'message': f"Affiliate strong: {affiliate_clicks} clicks!",
                'pattern': 'affiliate_placement_good',
                'success': True
            })
        else:
            learnings['insights'].append({
                'type': 'affiliate_warning',
                'message': f"Affiliate weak: {affiliate_clicks} clicks",
                'pattern': 'affiliate_placement_needs_work',
                'success': False
            })
        
        return learnings
    
    def update_learning_database(self, learnings: dict):
        """Store learnings for future reference"""
        for insight in learnings.get('insights', []):
            pattern = insight.get('pattern')
            success = insight.get('success')
            
            if success:
                # This pattern works - increase success rate
                db.update_learning_pattern(
                    pattern_name=pattern,
                    success_rate=95.0,  # High confidence
                    sample_size=1
                )
                logger.info(f"Pattern SUCCESS: {pattern}")
            else:
                # This pattern failed - mark as needs improvement
                db.update_learning_pattern(
                    pattern_name=pattern,
                    success_rate=20.0,  # Low confidence
                    sample_size=1
                )
                logger.info(f"Pattern NEEDS IMPROVEMENT: {pattern}")
    
    def get_optimization_recommendations(self, learnings: dict) -> list:
        """Based on learnings, what should next video do?"""
        recommendations = []
        
        for insight in learnings.get('insights', []):
            if not insight.get('success'):
                if 'thumbnail' in insight['type']:
                    recommendations.append({
                        'action': 'Redesign thumbnail',
                        'reason': insight['message'],
                        'priority': 'HIGH'
                    })
                elif 'script' in insight['type']:
                    recommendations.append({
                        'action': 'Improve script pacing',
                        'reason': insight['message'],
                        'priority': 'HIGH'
                    })
                elif 'engagement' in insight['type']:
                    recommendations.append({
                        'action': 'Strengthen CTA (Call-to-Action)',
                        'reason': insight['message'],
                        'priority': 'MEDIUM'
                    })
                elif 'affiliate' in insight['type']:
                    recommendations.append({
                        'action': 'Improve affiliate link placement',
                        'reason': insight['message'],
                        'priority': 'MEDIUM'
                    })
        
        return recommendations

# Create global instance
learning_engine = LearningEngine()
```
