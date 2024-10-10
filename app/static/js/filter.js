document.getElementById('searchInput').addEventListener('keyup', function() {
    let filter = this.value.toLowerCase();
    let links = document.querySelectorAll('#linksList .list-group-item');
    let hasMatches = false;

    links.forEach(function(link) {
        let title = link.querySelector('.h6').textContent.toLowerCase();
        let description = link.querySelector('span').textContent.toLowerCase();
        let category = link.querySelector('strong').textContent.toLowerCase();

        if (title.includes(filter) || description.includes(filter) || category.includes(filter)) {
            link.style.display = '';
            hasMatches = true;
        } else {
            link.style.display = 'none';
        }
    });

    document.getElementById('noResultsMessage').style.display = hasMatches ? 'none' : 'block';
});