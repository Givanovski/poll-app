def get_color(vote_count, total_votes):
    if total_votes == 0:
        return "#f8f9fa"  # Light gray for options with no votes
    elif vote_count == 0:
        return "#e9ecef"  # Slightly darker gray for options with zero votes
    else:
        # Calculate the percentage of votes for the option
        percentage = (vote_count / total_votes) * 100
        
        # Choose color based on percentage
        if percentage > 50:
            return "#28a745"  # Green for majority
        elif percentage > 20:
            return "#ffc107"  # Yellow for moderate
        else:
            return "#dc3545"  # Red for minority

