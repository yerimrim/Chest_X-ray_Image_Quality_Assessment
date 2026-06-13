const input = document.getElementById("images");

const preview = document.getElementById("preview");

input.addEventListener(
    "change",
    function () {
        preview.innerHTML = "";
        const files = this.files;
        if (files.length === 0) {
            return;
        }

        Array.from(files).forEach(
            function (file) {
                const reader = new FileReader();
                reader.onload =
                
                function (e) {
                    const container = document.createElement("div");
                    container.className = "preview-item";
                    container.innerHTML = `
                        <img src="${e.target.result}">
                        <p>${file.name}</p>
                    `;

                    preview.appendChild(container);
                };

                reader.readAsDataURL(file);
            }
        );
    }
);