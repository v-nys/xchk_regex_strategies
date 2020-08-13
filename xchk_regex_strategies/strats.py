import os
import regex
from xchk_core.strats import CheckingPredicate, OutcomeAnalysis, OutcomeComponent

class RegexCheck(CheckingPredicate):

    def __init__(self,pattern,pattern_description='een gekend patroon',name=None,extension=None):
        self.name = name
        self.pattern = pattern
        self.pattern_description = pattern_description
        # for student solution only
        self.extension = extension

    def _longest_partial_match(self,test_text,pattern):
        least_upper_bound = 0
        greatest_lower_bound = len(test_text)
        estimate = (least_upper_bound + greatest_lower_bound) // 2
        while least_upper_bound < greatest_lower_bound:
            partial_test_text = test_text[0:estimate]
            if pattern.fullmatch(partial_test_text,partial=True):
                least_upper_bound = estimate
                estimate = (estimate + greatest_lower_bound + 1) // 2
            else:
                greatest_lower_bound = estimate - 1
                estimate = (estimate + least_upper_bound) // 2
        return test_text[0:estimate]

    def entry(self,exercise_name):
        return f'{self.name or exercise_name}{"." if self.extension else ""}{self.extension or ""}'

    def mentioned_files(self,exercise_name):
        return set(self.entry(exercise_name))

    def instructions(self,exercise_name):
        return [f'Je bestand met naam {self.entry(exercise_name)} matcht met {self.pattern_description}']

    def negative_instructions(self,exercise_name):
        return [f'Je bestand met naam {self.entry(exercise_name)} matcht niet met {self.pattern_description}']

    def check_submission(self,submission,student_path,model_path,desired_outcome,init_check_number,parent_is_negation=False,open=open):
        with open(os.path.join(student_path,self.entry(submission.content_uid))) as fhs:
            fhs_contents = fhs.read()
            partial = self._longest_partial_match(fhs_contents,self.pattern)
            if partial != fhs_contents or not self.pattern.fullmatch(fhs_contents):
                overall_outcome = False
            else:
                overall_outcome = True
            if desired_outcome != overall_outcome:
                if partial != fhs_contents:
                    lines = partial.split('\n')
                    explanation = f"Je oplossing verschilt van {self.pattern_description} vanaf regel {len(lines)}, karakter {len(lines[-1])+1}."
                elif not self.pattern.fullmatch(fhs_contents):
                    explanation = f"Je oplossing is geen (volledige) match met {self.pattern_description}."
                else:
                    explanation = f"Je oplossing matcht volledig met {self.pattern_description} en dat is niet gewenst."
            else:
                explanation = None
            return OutcomeAnalysis(outcome=overall_outcome,
                                   outcomes_components=[OutcomeComponent(component_number=init_check_number,outcome=overall_outcome,desired_outcome=desired_outcome,renderer="text" if explanation else None,renderer_data=explanation,rendered_data=f'<p>{explanation}</p>' if explanation else "")])
