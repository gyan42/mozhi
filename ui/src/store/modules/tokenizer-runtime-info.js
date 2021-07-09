export default {
    namespaced: true,
    state: {
        originalText: "",
        separator: "\n",
        classes: [],
        inputSentences: [],
        annotations: [],
        currentClass: {},
        dataFrame: ''
    },
    getters: {

    },
    actions: {

    },
    mutations: {
        setInputSentences(state, payload) {
            if (!Array.isArray(payload)) {
                state.originalText = payload;
                payload = payload.split("\n");//(state.separator);
            }
            console.info(">>>>  setInputSentences")

            console.info(payload[0])
            // eslint-disable-next-line no-unused-vars
            state.inputSentences = payload.filter((s, i) => (s.length > 0)).map((s, i) => ({ id: i, text: s }));
            // state.inputSentences = payload.flatMap((s, i) => s.length > 1 ?  ({ id: i, text: s }) : {})
            console.info(state.inputSentences)
            console.info("<<<<  setInputSentences")
        },
        addClass(state, payload) {
            let existing = state.classes.find((c) => c.name == payload);
            if (existing) {
                return;
            }
            let lastIndex = state.classes.reduce((p, c) => {
                return c.id > p ? c.id : p;
            }, 0);
            state.classes.push({
                id: lastIndex + 1,
                name: payload,
            });
            if (state.classes.length === 1) {
                state.currentClass = state.classes[0];
            }
        },
        removeClass(state, payload) {
            state.classes = state.classes.filter((c) => c.id != payload);
            if (state.currentClass.id === payload) {
                state.currentClass = state.classes[0];
            }
        },
        setCurrentClass(state, payload) {
            state.currentClass = state.classes.find((c) => c.id === payload);
        },
        addAnnotation(state, payload) {
            state.annotations.push(payload);
        },
        setSeparator(state, payload) {
            state.separator = payload;
            const sentences = state.originalText.split(state.separator);
            state.inputSentences = sentences.map((s, i) => ({ id: i, text: s }));
        },
        setDataframe(state, payload) {
            state.dataframe = payload
        },
        resetClass(state, payload) {
            console.log("resetClass")
            console.log(payload)
            state.classes = []
        }
    }
}