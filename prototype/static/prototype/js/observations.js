hqDefine('prototype/js/observations.js', function () {
    function ObservationsViewModel(concepts) {
        var self = {};
        self.commcarehqFormQuestions = ko.observableArray();
        self.concepts = concepts;
        self.newConcept = ko.observable();
        self.observations = ko.observableArray();
        self.addObservation = function () {
            if (self.newConcept()) {
                var observation = {
                    concept: self.newConcept(),
                    source: ko.observable(),
                    allowsMultipleAnswers: ko.observable(false),
                };
                observation.answers = self.initAnswersForConcept(observation, self.newConcept());
                self.observations.push(observation);
            }
            self.newConcept(null);
        };
        self.initAnswersForConcept = function (parent, concept) {
            return _.map(concept.answers, function (answerConcept) {
                var answer = {
                    answerConcept: answerConcept,
                    answerSource: ko.observable(),
                    answerSourceValue: ko.observable(),
                    source: ko.computed(function () {
                        if (parent.allowsMultipleAnswers()) {
                            return answer.answerSource();
                        } else {
                            return parent.source();
                        }
                    })
                };
                return answer
            });
        };
        self.removeObservation = function (observation) {
            self.observations.remove(observation);
        };
        self.formatCalculate = function (calculate) {
            var caseRegex = new RegExp("instance\\('casedb'\\)/casedb/case\\[@case_id\\s=\\sinstance\\('commcaresession'\\)/session/data/case_id\\]", 'g');
            return calculate.replace(caseRegex, '#case');
        };
        return self;
    }
    return {
        ObservationsViewModel: ObservationsViewModel
    };
});
