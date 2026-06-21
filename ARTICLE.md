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

Once someone has a valid ID number, the doors that open are alarming. They can probe login pages and registration forms across services to see which ID numbers are active accounts, without ever triggering an invalid format error. They can walk through identity verification checks on government portals, insurance sites, and credit bureaus that treat a correct ID number as proof of identity. They can call your mobile carrier, recite the ID number, pass verification, and initiate a SIM swap, which gives them your one-time passwords, which gives them your bank account. They can register for government grants in your name, which is not a hypothetical because SASSA fraud has been front page news in South Africa for years and keeps getting more sophisticated. They can combine databases of valid ID numbers with common passwords for credential stuffing attacks tailored specifically to the South African market.

And the thing is, none of this requires hacking anything. The tool I built doesn't exploit a vulnerability in any system. It just does maths. The same maths a university student could do with a calculator and enough patience. All I did was make it fast enough that the scale of the problem becomes impossible to pretend doesn't exist.

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
