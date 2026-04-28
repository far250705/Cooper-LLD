import uuid
from datetime import datetime, timedelta


# -------------------- VOTER --------------------

class Voter:
    def __init__(self, name, age):
        self.voter_id = "VTR" + str(uuid.uuid4())[:5]
        self.name = name
        self.age = age
        self.has_voted = False

    def authenticate(self, voter_id):
        return self.voter_id == voter_id


# -------------------- CANDIDATE --------------------

class Candidate:
    def __init__(self, name, party):
        self.candidate_id = "CND" + str(uuid.uuid4())[:5]
        self.name = name
        self.party = party
        self.vote_count = 0

    def increment_vote(self):
        self.vote_count += 1


# -------------------- ELECTION --------------------

class Election:
    def __init__(self, title, duration_minutes=2):
        self.election_id = "ELC" + str(uuid.uuid4())[:5]
        self.title = title
        self.start_time = None
        self.end_time = None
        self.status = "CREATED"
        self.candidates = []

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def open_election(self):
        if len(self.candidates) < 2:
            print("❌ Need at least 2 candidates")
            return False

        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=2)
        self.status = "OPEN"
        print("✅ Election opened")
        return True

    def is_active(self):
        if self.status != "OPEN":
            return False
        now = datetime.now()
        return self.start_time <= now <= self.end_time

    def close_election(self):
        self.status = "CLOSED"

    def get_results(self):
        max_votes = max(c.vote_count for c in self.candidates)
        winners = [c for c in self.candidates if c.vote_count == max_votes]

        if len(winners) > 1:
            print("⚠️ Tie between:")
            for w in winners:
                print(w.name)
        else:
            winner = winners[0]
            print(f"🏆 Winner: {winner.name} | Votes: {winner.vote_count}")


# -------------------- VOTE RECORD --------------------

class VoteRecord:
    def __init__(self, voter_id, election_id):
        self.record_id = "REC" + str(uuid.uuid4())[:5]
        self.voter_id = voter_id
        self.election_id = election_id
        self.timestamp = datetime.now()


# -------------------- SYSTEM --------------------

class VotingSystem:
    def __init__(self):
        self.voters = {}
        self.elections = {}
        self.vote_records = []

    def register_voter(self, name, age):
        if age < 18:
            print("❌ Must be 18+")
            return None

        voter = Voter(name, age)
        self.voters[voter.voter_id] = voter
        print("✅ Registered:", voter.voter_id)
        return voter

    def create_election(self, title):
        election = Election(title)
        self.elections[election.election_id] = election
        print("✅ Election created:", election.election_id)
        return election

    def display_candidates(self, election_id):
        election = self.elections.get(election_id)
        if not election:
            print("❌ Invalid election")
            return

        print("\nCandidates:")
        for c in election.candidates:
            print(c.candidate_id, c.name, c.party)

    def cast_vote(self, voter_id, election_id, candidate_id):
        # -------- VALIDATIONS --------
        voter = self.voters.get(voter_id)
        if not voter:
            print("❌ Invalid Voter ID")
            return

        if voter.has_voted:
            print("❌ Already voted")
            return

        election = self.elections.get(election_id)
        if not election:
            print("❌ Invalid election")
            return

        if not election.is_active():
            print("❌ Voting closed or not started")
            return

        candidate = None
        for c in election.candidates:
            if c.candidate_id == candidate_id:
                candidate = c

        if not candidate:
            print("❌ Invalid candidate")
            return

        # -------- SAFE TRANSACTION --------
        try:
            candidate.increment_vote()
            voter.has_voted = True
            record = VoteRecord(voter_id, election_id)
            self.vote_records.append(record)
            print("✅ Vote recorded")

        except Exception as e:
            print("❌ Error occurred, retry:", e)

    def declare_results(self, election_id):
        election = self.elections.get(election_id)
        if not election:
            print("❌ Invalid election")
            return

        election.close_election()
        print("\n📊 Results:")
        for c in election.candidates:
            print(c.name, ":", c.vote_count)

        election.get_results()


# -------------------- MAIN --------------------

vs = VotingSystem()

while True:
    print("\n=== ONLINE VOTING SYSTEM ===")
    print("1.Register Voter")
    print("2.Create Election")
    print("3.Add Candidate")
    print("4.Open Election")
    print("5.View Candidates")
    print("6.Cast Vote")
    print("7.Declare Result")
    print("8.Exit")

    ch = int(input("Enter choice: "))

    if ch == 1:
        vs.register_voter(input("Name: "), int(input("Age: ")))

    elif ch == 2:
        vs.create_election(input("Election Title: "))

    elif ch == 3:
        eid = input("Election ID: ")
        name = input("Candidate Name: ")
        party = input("Party: ")
        vs.elections[eid].add_candidate(Candidate(name, party))

    elif ch == 4:
        eid = input("Election ID: ")
        vs.elections[eid].open_election()

    elif ch == 5:
        vs.display_candidates(input("Election ID: "))

    elif ch == 6:
        vs.cast_vote(
            input("Voter ID: "),
            input("Election ID: "),
            input("Candidate ID: ")
        )

    elif ch == 7:
        vs.declare_results(input("Election ID: "))

    else:
        break