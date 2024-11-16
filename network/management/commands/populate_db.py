from network.models import User, Followers, Likes, Posts
import random
from django.core.management.base import BaseCommand
from faker import Faker

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # Step 1: Create sample users
        users = list(set([Faker().first_name() for _ in range(550)]))
        created_users = []
        for i in range(len(users)):  # Creating 10 users
            user = User.objects.create_user(username=f"{users[i]}", password="password123")
            created_users.append(user)
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))

        # Step 2: Create sample posts for each user
        for user in created_users:
            for j in range(10):
                post = Posts.objects.create(
                    user=user,
                    post_title=f"Post Title {j + 1}",
                    post=f"This is post number {j + 1} by {user}\n{Faker().sentence()}",
                )
                self.stdout.write(self.style.SUCCESS(f"Created post: {post.post_title} by {user.username}"))

        # Step 3: Create sample followers (random following/follower relationships)
        for user in created_users:
            followers_count = random.randint(0, 100) 
            for _ in range(followers_count):
                follower = random.choice(created_users)
                if follower != user:
                    Followers.objects.create(user=user, follower=follower)
                    self.stdout.write(self.style.SUCCESS(f"{follower.username} is following {user.username}"))

        # Step 4: Create likes on posts
        for user in created_users:
            for _ in range(40):
                post = random.choice(Posts.objects.all())
                Likes.objects.create(user=user, fan=post.user)
                self.stdout.write(self.style.SUCCESS(f"{user} liked post '{post.post_title}' by {post.user.username}"))
        
        self.stdout.write(self.style.SUCCESS('Database populated with sample data!'))