595970246c9b8fa0a8000086


function capitalizeWord(word) {
  return word[0].toUpperCase() + word.slice(1);
}
______________________
const capitalizeWord = (word) => word.replace(word.charAt(0), word.charAt(0).toUpperCase());
______________________
const capitalizeWord = word => word[0].toUpperCase()+word.slice(1);
