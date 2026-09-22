/**
 * Controlador de Frontend para el Cuestionario Vocacional Interactivo
 */
document.addEventListener('DOMContentLoaded', () => {
    const steps = Array.from(document.querySelectorAll('.question-step'));
    const totalQuestions = steps.length;
    let currentStepIndex = 0;

    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressBadge = document.getElementById('progress-badge');
    const sectionIndicator = document.getElementById('section-indicator');
    const bubblesContainer = document.getElementById('bubbles-container');
    const answeredCountEl = document.getElementById('answered-count');
    const quizForm = document.getElementById('quiz-form');

    // Inicializar mapa de burbujas
    function initBubbles() {
        bubblesContainer.innerHTML = '';
        steps.forEach((step, idx) => {
            const bubble = document.createElement('button');
            bubble.type = 'button';
            bubble.id = `bubble-${idx}`;
            bubble.className = 'w-7 h-7 rounded-lg text-xs font-bold flex items-center justify-center transition-all bg-slate-100 text-slate-500 border border-slate-200 hover:border-brand-500';
            bubble.textContent = idx + 1;
            bubble.addEventListener('click', () => {
                showStep(idx);
            });
            bubblesContainer.appendChild(bubble);
        });
    }

    // Actualizar estados visuales de las burbujas y progreso
    function updateProgress() {
        let answeredCount = 0;
        steps.forEach((step, idx) => {
            const checkedInput = step.querySelector('input[type="radio"]:checked');
            const bubble = document.getElementById(`bubble-${idx}`);
            if (bubble) {
                if (checkedInput) {
                    answeredCount++;
                    bubble.className = 'w-7 h-7 rounded-lg text-xs font-bold flex items-center justify-center transition-all bg-emerald-500 text-white shadow-xs';
                } else if (idx === currentStepIndex) {
                    bubble.className = 'w-7 h-7 rounded-lg text-xs font-bold flex items-center justify-center transition-all bg-brand-600 text-white ring-2 ring-brand-300';
                } else {
                    bubble.className = 'w-7 h-7 rounded-lg text-xs font-bold flex items-center justify-center transition-all bg-slate-100 text-slate-500 border border-slate-200';
                }
            }
        });

        const percent = Math.round((answeredCount / totalQuestions) * 100);
        progressBar.style.width = `${Math.max(4, percent)}%`;
        progressBadge.textContent = `${percent}%`;
        progressText.textContent = `Pregunta ${currentStepIndex + 1} de ${totalQuestions}`;
        answeredCountEl.textContent = `${answeredCount} / ${totalQuestions} respondidas`;
    }

    // Mostrar el paso específico
    function showStep(index) {
        if (index < 0 || index >= totalQuestions) return;

        steps.forEach((step, idx) => {
            if (idx === index) {
                step.classList.remove('hidden');
                step.classList.add('animate-fade-in');
                const sectionName = step.dataset.section;
                sectionIndicator.textContent = sectionName;
            } else {
                step.classList.add('hidden');
                step.classList.remove('animate-fade-in');
            }
        });

        currentStepIndex = index;

        // Botón Anterior
        if (currentStepIndex === 0) {
            prevBtn.classList.add('hidden');
        } else {
            prevBtn.classList.remove('hidden');
        }

        // Botón Siguiente / Finalizar
        if (currentStepIndex === totalQuestions - 1) {
            nextBtn.classList.add('hidden');
            submitBtn.classList.remove('hidden');
        } else {
            nextBtn.classList.remove('hidden');
            submitBtn.classList.add('hidden');
        }

        updateProgress();
        window.scrollTo({ top: 120, behavior: 'smooth' });
    }

    // Manejar selección de opciones Likert
    steps.forEach((step, stepIdx) => {
        const cards = step.querySelectorAll('.likert-card');
        cards.forEach(card => {
            const radio = card.querySelector('input[type="radio"]');

            card.addEventListener('click', () => {
                // Desmarcar otras tarjetas en este paso
                cards.forEach(c => {
                    c.classList.remove('border-brand-600', 'bg-brand-50', 'ring-2', 'ring-brand-200', 'shadow-md');
                    c.classList.add('border-slate-200');
                });

                // Marcar tarjeta seleccionada
                card.classList.remove('border-slate-200');
                card.classList.add('border-brand-600', 'bg-brand-50', 'ring-2', 'ring-brand-200', 'shadow-md');
                radio.checked = true;

                updateProgress();

                // Auto-avanzar suavemente tras 350ms si no es la última
                if (stepIdx < totalQuestions - 1) {
                    setTimeout(() => {
                        showStep(stepIdx + 1);
                    }, 280);
                }
            });
        });
    });

    // Eventos de botones
    prevBtn.addEventListener('click', () => {
        if (currentStepIndex > 0) {
            showStep(currentStepIndex - 1);
        }
    });

    nextBtn.addEventListener('click', () => {
        const currentStep = steps[currentStepIndex];
        const checked = currentStep.querySelector('input[type="radio"]:checked');
        if (!checked) {
            alert('Por favor selecciona una opción antes de continuar.');
            return;
        }
        if (currentStepIndex < totalQuestions - 1) {
            showStep(currentStepIndex + 1);
        }
    });

    // Validación antes del envío
    quizForm.addEventListener('submit', (e) => {
        let unanswered = [];
        steps.forEach((step, idx) => {
            const checked = step.querySelector('input[type="radio"]:checked');
            if (!checked) {
                unanswered.push(idx + 1);
            }
        });

        if (unanswered.length > 0) {
            e.preventDefault();
            alert(`Aún te faltan responder las preguntas: ${unanswered.join(', ')}. Por favor complétalas para generar tu diagnóstico vocacional preciso.`);
            showStep(unanswered[0] - 1);
        }
    });

    // Inicializar
    initBubbles();
    showStep(0);
});
