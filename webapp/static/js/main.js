async function quickAnalyze() {
    const text = document.getElementById('quick-text').value.trim();
    if (!text) return;

    const btn = document.getElementById('quick-btn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-flex';
    btn.disabled = true;

    const formData = new FormData();
    formData.append('text', text);
    formData.append('remove_stopwords', document.getElementById('quick-stopwords').checked);

    try {
        const res = await fetch('/api/analyze', { method: 'POST', body: formData });
        const data = await res.json();
        if (!data.success) throw new Error(data.error);

        const s = data.statistics;
        document.getElementById('q-words').textContent = s.total_words;
        document.getElementById('q-unique').textContent = s.unique_words;
        document.getElementById('q-sentences').textContent = s.sentences;
        document.getElementById('q-sentiment').textContent = data.sentiment.sentiment_score.toFixed(2);

        const tags = document.getElementById('q-topwords');
        tags.innerHTML = data.frequencies.top_words.slice(0, 5).map(item =>
            `<span class="tag tag-neu">${item.word} (${item.count})</span>`
        ).join('');

        document.getElementById('quick-results').style.display = 'block';
    } catch (err) {
        console.error(err);
    } finally {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        btn.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('quick-text')?.addEventListener('input', () => {
        document.getElementById('quick-results').style.display = 'none';
    });
});
