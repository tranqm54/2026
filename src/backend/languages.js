
const LanguagesResources = {
    "en": {
        "main_title": "VIETNAMESE LUNAR NEW YEAR",
        "nav_intro": "Introduction",
        "nav_customs": "Customs",
        "nav_cuisine": "Cuisine",
        "nav_significance": "Significance"
    },
    "vi": {
        "main_title": "TẾT NGUYÊN ĐÁN VIỆT NAM",
        "nav_intro": "Giới thiệu",
        "nav_customs": "Phong tục",
        "nav_cuisine": "Ẩm thực",
        "nav_significance": "Ý nghĩa"
    }
};

class Languages {
    constructor(langMode = "vi") {
        this.langMode = langMode;
    }

    setMode(newMode) {
        if (newMode in LanguagesResources) {
            this.langMode = newMode;
        } else {
            console.error(`Language mode "${newMode}" not found!`);
        }
    }

    getDataLanguages() {
        return LanguagesResources[this.langMode] || {};
    }

    get(key) {
        const currentData = LanguagesResources[this.langMode];
        
        if (!currentData) {
            return `ERROR_LANG_NOT_SUPPORTED: ${this.langMode}`;
        }

        if (!(key in currentData)) {
            return `ERROR_KEY_NOT_FOUND: ${key}`;
        }

        return currentData[key];
    }

    updateUI() {
        const elements = document.querySelectorAll("[data-i18n]");
        elements.forEach(el => {
            const key = el.dataset.i18n;
            el.textContent = this.get(key);
        });
    }
}

export const translator = new Languages("vi");