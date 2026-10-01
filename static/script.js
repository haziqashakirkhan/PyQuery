const pdfInput = document.getElementById("pdfInput");
const fileList = document.getElementById("fileList");
const buildBtn = document.getElementById("buildBtn");
const uploadStatus = document.getElementById("uploadStatus");

const question = document.getElementById("question");
const askBtn = document.getElementById("askBtn");
const questionStatus = document.getElementById("questionStatus");

const answerContainer = document.getElementById("answerContainer");
const answer = document.getElementById("answer");
const sources = document.getElementById("sources");

const MAX_FILES = 5;

let selectedFiles = [];
let indexReady = false;


/* -----------------------------
   FILE SELECTION
----------------------------- */

pdfInput.addEventListener("change", () => {

    selectedFiles = Array.from(pdfInput.files);

    renderFiles();

    if (selectedFiles.length === MAX_FILES) {
        buildBtn.disabled = false;
        uploadStatus.textContent = "5 PDF files selected.";
    } else {
        buildBtn.disabled = true;

        uploadStatus.textContent =
            `Please select exactly ${MAX_FILES} PDF files.`;
    }
});


function renderFiles() {

    fileList.innerHTML = "";

    selectedFiles.forEach((file, index) => {

        const item = document.createElement("div");

        item.className = "file-item";

        item.textContent =
            `${index + 1}. ${file.name}`;

        fileList.appendChild(item);
    });
}


/* -----------------------------
   CREATE INDEX
----------------------------- */

buildBtn.addEventListener("click", async () => {

    if (selectedFiles.length !== MAX_FILES) {
        return;
    }

    buildBtn.disabled = true;

    uploadStatus.textContent =
        "Processing PDFs and creating embeddings...";

    const formData = new FormData();

    selectedFiles.forEach(file => {
        formData.append("files", file);
    });


    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });


        const data = await response.json();

        if (!response.ok) {
            const message = data.details || data.error || "Upload failed.";
            throw new Error(message);
        }


        indexReady = true;

        uploadStatus.textContent =
            `Study index ready. ${data.chunks ?? ""} chunks created.`;

        askBtn.disabled = false;

        questionStatus.textContent =
            "Study index ready";

    } catch (error) {

        console.error(error);

        uploadStatus.textContent =
            error.message || "Something went wrong while creating the study index.";

        buildBtn.disabled = false;
    }
});


/* -----------------------------
   ASK QUESTION
----------------------------- */

askBtn.addEventListener("click", askQuestion);


question.addEventListener("keydown", event => {

    if (event.key === "Enter" && event.ctrlKey) {
        askQuestion();
    }

});


async function askQuestion() {

    const userQuestion = question.value.trim();

    if (!userQuestion) {
        question.focus();
        return;
    }

    if (!indexReady) {
        return;
    }


    askBtn.disabled = true;

    askBtn.textContent = "Thinking...";

    answerContainer.classList.remove("hidden");

    answer.innerHTML =
        "<p>Searching your Python notes...</p>";

    sources.innerHTML = "";


    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: userQuestion
            })

        });

        const rawText = await response.text();
        let data;

        try {
            data = rawText ? JSON.parse(rawText) : {};
        } catch (error) {
            throw new Error(rawText || "Question request failed.");
        }

        if (!response.ok) {
            throw new Error(data.detail || data.error || data.answer || "Question request failed.");
        }

        answer.innerHTML = formatAnswer(data.answer || "The answer is not available in the uploaded documents.");


        renderSources(data.sources || []);


    } catch (error) {

        console.error(error);

        answer.innerHTML =
            "<p>Unable to get an answer. Please try again.</p>";

    } finally {

        askBtn.disabled = false;

        askBtn.textContent = "Ask PyQuery";

    }
}


/* -----------------------------
   ANSWER FORMATTER
----------------------------- */

function escapeHTML(text) {

    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}


function formatAnswer(text) {

    if (!text) {
        return "<p>No answer returned.</p>";
    }


    let safe = escapeHTML(text);


    /* Code blocks */

    safe = safe.replace(
        /```(?:python)?\s*([\s\S]*?)```/gi,
        "<pre><code>$1</code></pre>"
    );


    /* Inline code */

    safe = safe.replace(
        /`([^`]+)`/g,
        "<code>$1</code>"
    );


    /* Paragraphs */

    safe = safe
        .split(/\n{2,}/)
        .map(block => {

            if (
                block.trim().startsWith("<pre>") ||
                block.trim().startsWith("<code>")
            ) {
                return block;
            }

            return `<p>${block.replace(/\n/g, "<br>")}</p>`;
        })
        .join("");


    return safe;
}


/* -----------------------------
   SOURCES
----------------------------- */

function renderSources(sourceList) {

    if (!sourceList.length) {
        sources.innerHTML = "";
        return;
    }


    let html = `
        <div class="sources-title">
            RETRIEVED SOURCES
        </div>
    `;


    sourceList.forEach((source, index) => {

        const file =
            source.file ||
            source.source ||
            `Source ${index + 1}`;

        const page =
            source.page ||
            "";

        const text =
            source.text ||
            source.chunk ||
            "";


        html += `
            <div class="source-item">
                <strong>${escapeHTML(String(file))}</strong>

                ${page ? ` · Page ${escapeHTML(String(page))}` : ""}

                ${
                    text
                        ? `<div>${escapeHTML(
                            String(text).slice(0, 300)
                          )}...</div>`
                        : ""
                }
            </div>
        `;
    });


    sources.innerHTML = html;
}