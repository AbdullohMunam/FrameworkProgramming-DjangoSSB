import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from academy.models import Coach, Group, Player, TrainingSchedule


class Command(BaseCommand):
    help = 'Seed database with famous football players, coaches, age groups, and schedules'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data seeding...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        TrainingSchedule.objects.all().delete()
        Player.objects.all().delete()
        Group.objects.all().delete()
        Coach.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Seed coaches
        coaches = self.seed_coaches()
        self.stdout.write(self.style.SUCCESS(f'Created {len(coaches)} coaches'))
        
        # Seed groups
        groups = self.seed_groups(coaches)
        self.stdout.write(self.style.SUCCESS(f'Created {len(groups)} groups'))
        
        # Seed players
        players = self.seed_players(groups)
        self.stdout.write(self.style.SUCCESS(f'Created {len(players)} players'))
        
        # Seed schedules
        schedules = self.seed_schedules(groups)
        self.stdout.write(self.style.SUCCESS(f'Created {len(schedules)} schedules'))
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))

    def seed_coaches(self):
        """Create famous football coaches"""
        famous_coaches = [
            {'name': 'Pep Guardiola', 'license_level': 'UEFA Pro', 'phone': '+34-111-111-111'},
            {'name': 'Jurgen Klopp', 'license_level': 'UEFA Pro', 'phone': '+49-222-222-222'},
            {'name': 'Carlo Ancelotti', 'license_level': 'UEFA Pro', 'phone': '+39-333-333-333'},
            {'name': 'Diego Simeone', 'license_level': 'UEFA Pro', 'phone': '+34-444-444-444'},
            {'name': 'Antonio Conte', 'license_level': 'UEFA Pro', 'phone': '+39-555-555-555'},
            {'name': 'Thomas Tuchel', 'license_level': 'UEFA Pro', 'phone': '+49-666-666-666'},
        ]
        
        coaches = []
        for coach_data in famous_coaches:
            coach = Coach.objects.create(**coach_data)
            coaches.append(coach)
        
        return coaches

    def seed_groups(self, coaches):
        """Create age-based groups matching real-world youth academy categories"""
        age_groups = [
            {'name': 'U-10 (Under 10)', 'min_age': 8, 'max_age': 10},
            {'name': 'U-12 (Under 12)', 'min_age': 11, 'max_age': 12},
            {'name': 'U-14 (Under 14)', 'min_age': 13, 'max_age': 14},
            {'name': 'U-16 (Under 16)', 'min_age': 15, 'max_age': 16},
            {'name': 'U-18 (Under 18)', 'min_age': 17, 'max_age': 18},
            {'name': 'U-20 (Under 20)', 'min_age': 19, 'max_age': 20},
        ]
        
        groups = []
        for i, group_data in enumerate(age_groups):
            # Assign coaches in round-robin fashion
            coach = coaches[i % len(coaches)]
            group = Group.objects.create(
                name=group_data['name'],
                coach=coach
            )
            # Store age range for later use
            group.min_age = group_data['min_age']
            group.max_age = group_data['max_age']
            groups.append(group)
        
        return groups

    def seed_players(self, groups):
        """Create famous football players with realistic ages distributed across groups"""
        famous_players = [
            # Goalkeepers
            {'name': 'Gianluigi Buffon', 'position': 'Goalkeeper'},
            {'name': 'Manuel Neuer', 'position': 'Goalkeeper'},
            {'name': 'Alisson Becker', 'position': 'Goalkeeper'},
            {'name': 'Thibaut Courtois', 'position': 'Goalkeeper'},
            {'name': 'Ederson Moraes', 'position': 'Goalkeeper'},
            {'name': 'Marc-André ter Stegen', 'position': 'Goalkeeper'},
            
            # Defenders
            {'name': 'Sergio Ramos', 'position': 'Defender'},
            {'name': 'Virgil van Dijk', 'position': 'Defender'},
            {'name': 'Gerard Piqué', 'position': 'Defender'},
            {'name': 'Thiago Silva', 'position': 'Defender'},
            {'name': 'Marcelo Vieira', 'position': 'Defender'},
            {'name': 'Dani Alves', 'position': 'Defender'},
            {'name': 'Giorgio Chiellini', 'position': 'Defender'},
            {'name': 'Kalidou Koulibaly', 'position': 'Defender'},
            {'name': 'Raphael Varane', 'position': 'Defender'},
            {'name': 'Andrew Robertson', 'position': 'Defender'},
            {'name': 'Trent Alexander-Arnold', 'position': 'Defender'},
            {'name': 'Joao Cancelo', 'position': 'Defender'},
            
            # Midfielders
            {'name': 'Luka Modrić', 'position': 'Midfielder'},
            {'name': 'Kevin De Bruyne', 'position': 'Midfielder'},
            {'name': 'N\'Golo Kanté', 'position': 'Midfielder'},
            {'name': 'Toni Kroos', 'position': 'Midfielder'},
            {'name': 'Paul Pogba', 'position': 'Midfielder'},
            {'name': 'Joshua Kimmich', 'position': 'Midfielder'},
            {'name': 'Casemiro', 'position': 'Midfielder'},
            {'name': 'Frenkie de Jong', 'position': 'Midfielder'},
            {'name': 'Marco Verratti', 'position': 'Midfielder'},
            {'name': 'Jorginho', 'position': 'Midfielder'},
            {'name': 'Pedri', 'position': 'Midfielder'},
            {'name': 'Gavi', 'position': 'Midfielder'},
            {'name': 'Bruno Fernandes', 'position': 'Midfielder'},
            {'name': 'Bernardo Silva', 'position': 'Midfielder'},
            
            # Forwards
            {'name': 'Cristiano Ronaldo', 'position': 'Forward'},
            {'name': 'Lionel Messi', 'position': 'Forward'},
            {'name': 'Neymar Jr', 'position': 'Forward'},
            {'name': 'Robert Lewandowski', 'position': 'Forward'},
            {'name': 'Kylian Mbappé', 'position': 'Forward'},
            {'name': 'Erling Haaland', 'position': 'Forward'},
            {'name': 'Karim Benzema', 'position': 'Forward'},
            {'name': 'Harry Kane', 'position': 'Forward'},
            {'name': 'Mohamed Salah', 'position': 'Forward'},
            {'name': 'Sadio Mané', 'position': 'Forward'},
            {'name': 'Sergio Agüero', 'position': 'Forward'},
            {'name': 'Luis Suárez', 'position': 'Forward'},
            {'name': 'Romelu Lukaku', 'position': 'Forward'},
            {'name': 'Antoine Griezmann', 'position': 'Forward'},
            {'name': 'Eden Hazard', 'position': 'Forward'},
            {'name': 'Raheem Sterling', 'position': 'Forward'},
            {'name': 'Son Heung-min', 'position': 'Forward'},
            {'name': 'Vinicius Jr', 'position': 'Forward'},
        ]
        
        players = []
        for player_data in famous_players:
            # Randomly select a group
            group = random.choice(groups)
            # Generate age within the group's range
            age = random.randint(group.min_age, group.max_age)
            
            # Create username from name (lowercase, remove spaces)
            username = player_data['name'].lower().replace(' ', '').replace('\'', '')
            email = f"{username}@ssbacademy.com"
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password='player123'  # Default password for all seeded players
            )
            
            # Create player (approved status)
            player = Player.objects.create(
                user=user,
                name=player_data['name'],
                age=age,
                position=player_data['position'],
                group=group,
                status=Player.STATUS_APPROVED,
                approved_at=datetime.now()
            )
            players.append(player)
        
        return players

    def seed_schedules(self, groups):
        """Create training schedules for each group"""
        schedules = []
        
        # Generate schedules for the next 4 weeks
        start_date = datetime.now().date()
        
        # Training days: Monday, Wednesday, Friday
        training_days = [0, 2, 4]  # 0=Monday, 2=Wednesday, 4=Friday
        
        # Training times for different age groups
        training_times = [
            '15:00',  # 3 PM
            '16:30',  # 4:30 PM
            '18:00',  # 6 PM
        ]
        
        for week in range(4):  # 4 weeks
            for day_offset in training_days:
                # Calculate the date
                days_ahead = week * 7 + day_offset
                schedule_date = start_date + timedelta(days=days_ahead)
                
                # Skip if date is in the past
                if schedule_date < start_date:
                    continue
                
                # Assign different times to different groups
                for i, group in enumerate(groups):
                    time = training_times[i % len(training_times)]
                    
                    schedule = TrainingSchedule.objects.create(
                        date=schedule_date,
                        time=time,
                        group=group
                    )
                    schedules.append(schedule)
        
        return schedules
