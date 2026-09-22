/**
 * Renderizado de Gráficos Vocacionales con Chart.js
 */
function renderVocationalCharts(riasecData, skillsData) {
    // 1. Gráfico Radar RIASEC
    const radarCtx = document.getElementById('riasecRadarChart');
    if (radarCtx && riasecData) {
        new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: [
                    'Realista (R)',
                    'Investigativo (I)',
                    'Artístico (A)',
                    'Social (S)',
                    'Emprendedor (E)',
                    'Convencional (C)'
                ],
                datasets: [{
                    label: 'Afinidad Vocacional (%)',
                    data: [
                        riasecData.percentages.R || 0,
                        riasecData.percentages.I || 0,
                        riasecData.percentages.A || 0,
                        riasecData.percentages.S || 0,
                        riasecData.percentages.E || 0,
                        riasecData.percentages.C || 0
                    ],
                    backgroundColor: 'rgba(99, 102, 241, 0.25)',
                    borderColor: 'rgba(79, 70, 229, 1)',
                    pointBackgroundColor: 'rgba(79, 70, 229, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(79, 70, 229, 1)',
                    pointRadius: 4,
                    borderWidth: 2.5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(203, 213, 225, 0.6)' },
                        grid: { color: 'rgba(226, 232, 240, 0.8)' },
                        pointLabels: {
                            font: { size: 11, weight: 'bold', family: 'Plus Jakarta Sans' },
                            color: '#334155'
                        },
                        ticks: {
                            beginAtZero: true,
                            max: 100,
                            stepSize: 20,
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw}% de afinidad`;
                            }
                        }
                    }
                }
            }
        });
    }

    // 2. Gráfico de Barras Horizontales para Habilidades
    const barCtx = document.getElementById('skillsBarChart');
    if (barCtx && skillsData) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: [
                    'Lógico-Matemática',
                    'Verbal y Comunicación',
                    'Espacial y Creativa',
                    'Interpersonal y Liderazgo',
                    'Técnica y Manual',
                    'Científica e Investigación'
                ],
                datasets: [{
                    label: 'Nivel Autopercibido (%)',
                    data: [
                        skillsData.percentages.logic_math || 0,
                        skillsData.percentages.verbal || 0,
                        skillsData.percentages.spatial_creative || 0,
                        skillsData.percentages.social_leadership || 0,
                        skillsData.percentages.technical_manual || 0,
                        skillsData.percentages.scientific_research || 0
                    ],
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(6, 182, 212, 0.8)',
                        'rgba(236, 72, 153, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(139, 92, 246, 0.8)'
                    ],
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(226, 232, 240, 0.6)' },
                        ticks: {
                            callback: function(value) { return value + "%"; },
                            font: { family: 'Plus Jakarta Sans', size: 10 }
                        }
                    },
                    y: {
                        grid: { display: false },
                        ticks: {
                            font: { weight: 'bold', family: 'Plus Jakarta Sans', size: 11 },
                            color: '#334155'
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Nivel: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }
}
