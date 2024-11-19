document.addEventListener("DOMContentLoaded", () => {
    // Like/Unlike button functionality
    const likeButtons = document.querySelectorAll(".like_button");

    likeButtons.forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;
            const action = button.value;

            // AJAX GET request to like/unlike the post
            fetch(`/like?id=${id}&action=${action}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(result => {
                // Update the like count in the UI
                const likeCountElement = document.querySelector(`#like-count-${id}`);
                if (result.like_count !== undefined) {
                    likeCountElement.textContent = result.like_count;
                }

                // Toggle the button text between Like/Unlike based on the action
                if (action === "like") {
                    button.value = "unlike";
                    button.textContent = "Unlike";
                } else {
                    button.value = "like";
                    button.textContent = "Like";
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // Edit button functionality
    const editButtons = document.querySelectorAll(".edit-button");

    editButtons.forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;
            const titleElement = document.querySelector(`.title-${id}`);
            const bodyElement = document.querySelector(`.body-${id}`);

            // Get the current content of the post
            const titleText = titleElement.textContent.trim();
            const bodyText = bodyElement.textContent.trim();

            // Replace title and body with input fields for editing
            const titleInput = document.querySelector(".post-title");
            const bodyInput = document.querySelector(".post-content");

            // Set current values to the form
            titleInput.value = titleText;
            bodyInput.value = bodyText;
            bodyInput.focus();

            // Change the button to "Save"
            button.textContent = "Save";
            const submitButton = document.querySelector("#submit");
            submitButton.value = "Save";

            // Function to handle save
            const savePost = (event) => {
                event.preventDefault(); // Prevent form submission

                // AJAX POST request to update the post
                fetch(`/edit/${id}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": "{{ csrf_token }}"  // Ensure CSRF token is included
                    },
                    body: JSON.stringify({
                        post_title: titleInput.value,
                        post: bodyInput.value
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.message === "successfully editted the message") {
                        // Update the content in the UI
                        titleElement.textContent = titleInput.value;
                        bodyElement.textContent = bodyInput.value;
                        button.textContent = "Edit";
                        titleInput = '';
                        bodyInput = '';

                        submitButton.removeEventListener("click", savePost);
                        button.removeEventListener("click", savePost);
                    } else {
                        alert("An error occurred while updating the post.");
                    }
                })
                .catch(error => console.error("Error:", error));
            };

            submitButton.removeEventListener("click", savePost);
            submitButton.addEventListener("click", savePost);
            button.removeEventListener("click", savePost);
            button.addEventListener("click", savePost);
        });
    });
});
