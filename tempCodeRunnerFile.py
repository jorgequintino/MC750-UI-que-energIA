        left_value = 0 if new_stage == 0 else self.milestones[new_stage - 1]
        right_value = self.milestones[new_stage] if new_stage < len(self.milestones) else self.milestones[-1]

        self.left_milestone_label.configure(text=f"{left_value:.2f} Wh")
        self.right_milestone_label.configure(text=f"{right_value:.2f} Wh")