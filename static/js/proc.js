document.addEventListener('DOMContentLoaded', function() {
    const checkboxDefinitions = document.getElementById('checkbox-definitions');
    const checkboxTranslations = document.getElementById('checkbox-translations');
    const rows = document.querySelectorAll('.partitioned-table tbody tr'); 
    const thead = document.querySelector('.partitioned-table thead'); 
    
    function toggleDefinitionsVisibility() {
        const definitionHeader = thead.querySelector('th:nth-child(3)'); 
        if (definitionHeader) {
            if (checkboxDefinitions.checked) {
                definitionHeader.style.display = 'none';
            } else {
                definitionHeader.style.display = 'table-cell'; 
            }
        }

        rows.forEach(row => {
            const definitionCell = row.querySelector('td:nth-child(3)'); 
            if (definitionCell) {
                if (checkboxDefinitions.checked) {
                    definitionCell.style.display = 'none';
                } else {
                    definitionCell.style.display = 'table-cell'; 
                }
            }
        });
    }

    function toggleTranslationsVisibility() {
        rows.forEach(row => {
            const translationCell = row.querySelector('td:nth-child(4)'); 
            
            if (translationCell) {
                if (checkboxTranslations.checked) {
                    translationCell.style.display = 'none';
                } else {
                    translationCell.style.display = 'table-cell'; 
                }
            }
        });

        const translationHeader = thead.querySelector('th:nth-child(4)'); 
        if (translationHeader) {
            if (checkboxTranslations.checked) {
                translationHeader.style.display = 'none';
            } else {
                translationHeader.style.display = 'table-cell'; 
            }
        }
    }

    checkboxDefinitions.addEventListener('change', toggleDefinitionsVisibility);
    checkboxTranslations.addEventListener('change', toggleTranslationsVisibility);

    toggleDefinitionsVisibility();
    toggleTranslationsVisibility();
});
