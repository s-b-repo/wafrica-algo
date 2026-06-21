I Generated 900 Million Valid South African ID Numbers to Prove a Point

Your ID number was never a secret. Here's why that should worry you.


I've always been the kind of person who needs to know how things work. Not just the surface level stuff, but the actual mechanics underneath. So when I started looking into how South African ID numbers are structured, I went down a rabbit hole that ended with me generating every single valid ID number that could ever exist. All 900 million of them. On a regular laptop. In under an hour.

What started as curiosity turned into something that genuinely concerned me.


What's actually in your ID number

Most people just memorize their ID number and never think twice about what it contains. But every digit means something.

Take any 13-digit SA ID number. The first six digits are your date of birth, year month day. The next four digits are a sequence number that also tells someone your gender, with 0000 through 4999 being female and 5000 through 9999 being male. Digit eleven is your citizenship status, zero for South African citizens and one for permanent residents. Digit twelve used to represent race back before 1980, but now it's just permanently set to 8. And that last digit, number thirteen, is a check digit calculated using something called the Luhn algorithm.

So think about that for a second. If I know your birthday and your gender, I already know 10 out of 13 digits. The 11th is almost certainly 0. The 12th is always 8. The 13th is just maths based on the other 12.

That's not a secure identifier. That's basically a trivia question about you.


The Luhn algorithm and why it doesn't protect you

The Luhn algorithm was invented in 1954 by an IBM scientist named Hans Peter Luhn. It was designed to catch typos and accidental errors when people wrote down numbers by hand. It was never, ever intended to be a security mechanism.

The way it works is pretty straightforward. You take the first 12 digits of the ID. Starting from the right side, you double every second digit. If doubling gives you something over 9, you subtract 9. Then you add everything up. Whatever number you need to tack on to make the total divisible by 10, that's your check digit.

It's the same formula that validates your credit card number. Ten lines of Python code. Completely deterministic. Give me the first 12 digits and I can tell you the 13th one every single time without fail.

There's no encryption involved. No randomness. No secret sauce. Just basic arithmetic that a calculator could handle.

There's also an interesting footnote here. Apparently, according to research by Ryan Neil Parker, the Department of Home Affairs implemented this algorithm backwards, processing digits from left to right instead of the standard right to left. Nobody can say for certain whether that was intentional, a workaround, or just a mistake from decades ago. The internet calls it the SA ID Fumble. The fact that nobody really knows tells you something about how much serious scrutiny this system has received over the years.


Building the generator and the bug that almost ruined everything

My first attempt at building this was painfully slow. One loop in Python, checking every possible combination one by one. 126 years of dates, roughly 365 days per year, 10,000 sequence numbers per day, 2 citizenship options. That works out to around 920 million combinations. With the za-id-number Python library validating each one individually, creating a whole object for every single ID, parsing dates, computing gender, I was looking at literal days of runtime.

So I reworked it. Two changes made all the difference.

First, I split the work across multiple CPU cores. January 1985 has nothing to do with February 1985, so there's no reason they can't be computed at the same time. I broke everything into 1,524 monthly chunks and spread them across every core on the machine.

Second, I got rid of the external library entirely. We're already generating valid dates and computing correct check digits ourselves. Every ID we produce is valid by construction. Paying for a full Python object instantiation for each of 900 million IDs is like hiring an accountant to confirm that 2 plus 2 equals 4.

I replaced all of it with a tiny inline Luhn verifier. No objects, no date parsing, just the raw calculation. 7 times faster.

The end result was pretty dramatic. A full year's worth of IDs, 7.3 million numbers, generates in about 3 seconds on a 12-core machine. The whole dataset from 1900 to 2026, all 927 million IDs, takes under an hour.

But here's where things almost went sideways. I nearly shipped the entire tool with every single output being wrong.

My Luhn implementation was doubling the wrong digit positions. Even indices instead of odd. In the code, the difference is literally one character. One equals sign pointing at the wrong number. Every ID the tool spit out had the right format, 13 digits, valid dates, proper structure, but they all had incorrect check digits. They looked perfect to the naked eye and they passed all my own format checks.

I only caught it because I copy-pasted one of the generated IDs into an online validator and saw the word Invalid staring back at me.

One character. That was the margin between a working tool and a tool that produces 900 million pieces of convincing garbage. If I had only tested against my own code, I never would have caught it.

That experience burned a lesson into my brain. Never validate your output using only the logic that produced it. Always check against something external.


Making it something people can actually use

The original script was the kind of thing you write at 2 in the morning. Everything hardcoded. Want to change the year range? Edit the source code. Want just 200 IDs instead of 900 million? Too bad, edit the source code. No progress indicator while it runs, so you just sit there wondering if it crashed.

I added a proper command line interface. Now you can specify the year range, the output file, how many workers to use, how many IDs you want, and whether to run validation. There's a dry run flag that tells you the estimated output size before you commit to anything, which matters when the full output is 12 gigabytes.

During generation you get a live progress line showing the percentage done, total count, and how fast it's going. Watching it tick along at 2 million IDs per second is honestly pretty satisfying.


Now here's the part that should make you uncomfortable

Everything up to this point was a fun engineering problem. Algorithm implementation, performance optimization, CLI design. Interesting stuff for a developer.

But the implications of what this tool demonstrates are genuinely unsettling, and I think they need to be talked about a lot more than they are.

Your ID number is not just some random number on a card. In South Africa, it is the master key to your entire life. Want to open a bank account? ID number. Get a cell phone contract? ID number. File taxes? ID number. Apply for a SASSA grant? ID number. Register to vote? ID number. Run a credit check? ID number.

And in a disturbing number of these systems, the ID number by itself is enough to get through the door. No second factor. No fingerprint. No one-time pin. Just thirteen digits and the system treats you like you're who you claim to be, or at least lets you look around enough to do damage.

Let me put some numbers on this to make the scale clear.

Say I want to find your specific ID number. I know you're a woman born sometime between 1990 and 1995. You're a South African citizen. That's the kind of information anyone could pick up from a LinkedIn profile, a Facebook page, or a five-minute conversation.

With those constraints, the search space drops to about 36 million possibilities. My generator cranks out over 2 million IDs per second.

That means I can find your ID number in 18 seconds.

Not hours. Not days. Eighteen seconds on a laptop.

Once someone has a valid ID number, the doors that open are alarming. Let me walk through two of the most damaging scenarios in detail, because I think people underestimate how straightforward these attacks actually are.


How a SIM swap works with just an ID number

This is the one that drains bank accounts, and it happens in South Africa every single day.

It starts with a phone call. The attacker calls your mobile carrier, Vodacom, MTN, Cell C, whoever you're with. They say they've lost their phone and need a replacement SIM. The consultant on the other end asks them to verify their identity. In many cases, the verification is your full name and your ID number. Sometimes they ask for your address or the last recharge amount, but the ID number is the anchor of the whole process.

The attacker provides the generated ID number. It's valid. It passes the format check on the consultant's screen. Combined with a name, which is trivially available from social media, LinkedIn, or even just a data breach, the consultant has no reason to doubt them.

A new SIM gets activated on your number. Your phone goes dead. You might not notice for a few hours, especially if it happens at night.

Now the attacker has your phone number. Every OTP, every two-factor authentication SMS, every bank notification, all of it goes to them. They log into your banking app. They reset the password using SMS verification. They transfer money out. By the time you wake up and realize your phone has no signal, your account has been cleaned out.

The entire chain of events, from generated ID number to emptied bank account, relies on one broken assumption at the very first step: that knowing an ID number proves you are that person. It doesn't. It never did. But the carrier's verification process treats it like it does.

Some carriers have added additional checks in recent years, like requiring you to visit a store with your physical ID document. But phone-based SIM swaps still happen constantly. The Banking Risk Information Centre reported that SIM swap fraud in South Africa increased by over 400 percent in recent years, with losses running into hundreds of millions of rands annually.

The fix is not complicated. Carriers should require in-person verification with biometrics for any SIM change. Banks should stop relying on SMS-based OTPs as the primary second factor and move to app-based authentication or hardware tokens. And critically, no step in this chain should treat an ID number as a secret, because as this tool demonstrates, it is not one.


How SASSA grant fraud works with generated ID numbers

The South African Social Security Agency administers grants to millions of vulnerable people. Old age pensions, disability grants, child support grants, the R350 Social Relief of Distress grant. These are lifelines for people who have nothing else.

The system was designed to be accessible, which is the right instinct. You shouldn't need a law degree to apply for a grant that feeds your children. But accessible and unprotected are different things, and the grant system has struggled to tell them apart.

Here is how it has been exploited.

The attacker generates a batch of valid ID numbers using a tool like this one. They don't need specific targets. They just need ID numbers that belong to real people who are eligible for grants but haven't applied yet, or in some cases, ID numbers that belong to people who have already died but haven't been removed from the population register.

They submit applications through the SASSA channels, online, via USSD, or through intermediaries who process applications in bulk in rural areas. The ID number is the primary identifier in the application. If it's valid and it matches a record in the Department of Home Affairs database, the application moves forward.

For the SRD grant specifically, the R350 one, verification has historically been minimal. The system checks the ID number against the Home Affairs database to confirm the person exists, checks whether they're already receiving another grant or have employment income through UIF records, and if those checks pass, the grant gets approved. For much of the system's history, there was no biometric verification at the application stage.

The money gets paid out to a bank account or a post office cash collection point. The attacker either provides their own banking details, or they use a network of mules to collect cash payments. In some cases, corrupt insiders at SASSA offices or the Post Office have facilitated bulk fraudulent applications.

The scale of this problem is not theoretical. In 2022, SASSA itself admitted that millions of fraudulent SRD grant applications had been detected. News reports have documented cases of single individuals linked to hundreds of fraudulent grant applications. The Special Investigating Unit has been running ongoing investigations into SASSA fraud for years, with criminal cases involving billions of rands.

The people who suffer most are the actual beneficiaries. When the fraud budget balloons, the system tightens restrictions, adds delays, and makes the application process harder for everyone. Legitimate applicants get declined because the system flagged something. Payments get delayed while investigations run. The people who need R350 to eat this week get caught in a dragnet designed to catch criminals who gamed the system with nothing more than a list of valid numbers.

What should change is straightforward but requires political will. Biometric verification at the point of application, not just at collection. Cross-referencing applications against death records in real time, not in batch jobs that run weeks behind. Linking grant payments to verified bank accounts that have themselves been opened with in-person identity verification. And fundamentally, stopping the practice of treating a valid ID number as sufficient proof that the person standing in front of you, or more often the person on the other end of a USSD session, is who they claim to be.


These two scenarios, SIM swaps and grant fraud, are not edge cases. They are not theoretical risks discussed in academic papers that nobody reads. They are happening right now, at industrial scale, across South Africa. And both of them start the same way: with a valid 13-digit number that the system was never designed to treat as a secret but does anyway.

None of this requires hacking anything. The tool I built doesn't exploit a vulnerability in any system. It just does arithmetic. The same arithmetic a university student could do with a calculator and a free afternoon. All I did was make it fast enough that the scale of the problem becomes impossible to pretend doesn't exist.

The real vulnerability here is not my generator. The real vulnerability is that sixty million people's access to banking, healthcare, telecommunications, and government services is gated by a number with roughly 30 bits of entropy. For some context, that's less randomness than a 9-character password. And unlike a password, you can never change it. It's yours for life.

The SA ID number was designed in the 1960s as a way to identify people on paper forms. It was meant to be written on documents, spoken over the phone, printed on laminated cards. It was an identifier, the same category as a name or a postal address. Nobody intended it to be proof of identity. But over the decades, digital systems co-opted it as exactly that, because it was convenient. And nobody stopped to ask whether convenient and secure were the same thing.

They are not.


What actually needs to change

These are not easy fixes and I'm not pretending they are. But they are necessary and overdue.

Stop treating ID numbers like passwords. They identify you. They do not prove you are you. Any system that treats a correct ID number as sufficient verification is broken by design, full stop.

Add multi-factor authentication to everything. If the only thing between a fraudster and someone's savings account is 13 predictable digits, that is not security. That is a polite suggestion. Biometrics, OTPs, hardware tokens, anything. Just add something.

Detect and block enumeration. If an IP address is querying ten thousand ID numbers per minute against your API, that is not a customer. That is an attack. Rate limit it. Flag it. Investigate it.

Tokenise the number. Stop passing raw ID numbers between systems like we're still faxing things. Use tokenised references that are meaningless outside their original context. The financial industry figured this out with credit card numbers years ago. There's no reason ID numbers should be any different.

Acknowledge the problem publicly. SIM swap fraud costs South Africans hundreds of millions of rands every year. Grant fraud is a recurring national scandal. The 13-digit ID number system is not equipped for the digital world it's being asked to secure, and pretending otherwise doesn't protect a single person.


Why I published this

I published this tool because I believe awareness forces action, and polite silence doesn't.

Every valid ID number this generator produces could be computed by hand by anyone who can read the publicly documented format and do basic arithmetic. I didn't discover a secret. I didn't crack a code. I pointed at a door that was never locked and said, hey, that door was never locked.

My hope is that this pushes the conversation forward. That the next time a bank or telco or government department designs a verification flow, someone in the room says, the ID number alone is not enough. That engineers building South African systems start treating the ID number like what it is, a public identifier, not a secret.

Until that shift happens, sixty million South Africans are trusting their digital lives to thirteen digits and the assumption that nobody will bother doing the maths.

I did the maths. It took 18 seconds.


For developers, the legitimate use cases

This tool has practical, constructive applications beyond proving a security point.

If you're building anything that accepts SA ID numbers, you need valid test data that covers the edge cases. Leap years. February 29th birthdays. Boundary dates at the start and end of months. Both citizenship values. The full gender sequence range. Real validators need real test data, and making it up by hand doesn't scale.

You can also use the output to validate your own ID checking logic. Run your validator against a known-good dataset and see if it accepts everything it should and rejects everything it shouldn't.

For authorized penetration testing engagements, this provides the kind of test data you need to assess how systems handle valid but unauthorized ID number submissions.

And for academic work, there's genuine research value in analyzing the entropy characteristics, check digit distributions, and structural predictability of national ID schemes.

The repo is at github.com/s-b-repo/wafrica-algo if you want to look at the code or run it yourself. It's pure Python, no dependencies, runs on anything with Python 3.7 or later.


What I took away from all of this

The Luhn algorithm shows up everywhere once you start looking. Credit cards, IMEI numbers on phones, national ID systems. Understanding how it works opens up a whole family of validation systems to examination.

Getting one character wrong in the implementation was the difference between 900 million valid IDs and 900 million convincing fakes. Testing against your own code isn't testing. You have to validate against something external.

Making something fast changes what it means. A script that runs for a week is an academic curiosity. A tool that finishes in an hour is a demonstration of a real problem. The underlying maths is identical. The impact is completely different.

And most importantly, convenience is how security fails. ID numbers didn't become authenticators because they're secure. They became authenticators because they were easy. That's how most security problems start, not with a sophisticated attack, but with a shortcut nobody questioned until it was too late.


Built with Python. Validated against real-world SA ID checkers. Published because the maths was always public, and now the conversation should be too.
