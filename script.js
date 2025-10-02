document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada com sucesso!");

    // Exemplo de interatividade: rolagem suave para links internos
    document.querySelectorAll("nav a").forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();

            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70, // Ajuste para o cabeçalho fixo, se houver
                    behavior: "smooth"
                });
            }
        });
    });
});
