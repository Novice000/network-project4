from network.models import User, Followers, Likes, Posts
import random
from django.core.management.base import BaseCommand
from faker import Faker

class Command(BaseCommand):
    help = "Populates the database with sample data for users, posts, followers, and likes"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Step 1: Create sample users
        users = list(set([fake.first_name() for _ in range(300)]))
        created_users = []

        for username in users:
            user = User.objects.create_user(username=username, password="password123")
            created_users.append(user)
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))

        # Step 2: Create sample posts for each user
        for user in created_users:
            for j in range(10):
                post = Posts.objects.create(
                    user=user,
                    post_title=f"Post Title {j + 1}",
                    post=f"This is post number {j + 1} by {user.username}\n{fake.sentence()}",
                )
                self.stdout.write(self.style.SUCCESS(f"Created post: {post.post_title} by {user.username}"))

        # Step 3: Create sample followers (random following/follower relationships)
        for user in created_users:
            followers_count = random.randint(0, 50) 
            followers_set = set()

            for _ in range(followers_count):
                while True:
                    follower = random.choice(created_users)
                    if follower != user and follower not in followers_set:
                        followers_set.add(follower)
                        break

                Followers.objects.create(user=user, follower=follower)
                self.stdout.write(self.style.SUCCESS(f"{follower.username} is following {user.username}"))

        # Step 4: Create likes on posts
        for user in created_users:
            for _ in range(25):
                post = random.choice(Posts.objects.all())

                # Check if the user has already liked the post
                if not Likes.objects.filter(user=user, post=post).exists():
                    Likes.objects.create(user=user, post=post)
                    post.like_count += 1  # Update the likes count
                    post.save()
                    self.stdout.write(self.style.SUCCESS(f"{user.username} liked post '{post.post_title}' by {post.user.username}"))

        self.stdout.write(self.style.SUCCESS('Database populated with sample data!'))
