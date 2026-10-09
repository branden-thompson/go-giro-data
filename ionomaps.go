package ionomaps

import (
	"context"
	"errors"
	"time"

	"github.com/branden-thompson/go-ionomaps/internal/terms"
)

// Fetcher is the host's network: the library opens no connection of its own
// (R-5.1). It asks one address, with the validators of the last answer, and
// hands back the status, the rate headers and the body. It must not retry a
// 429: the library alone decides a back-off.
type Fetcher interface {
	Fetch(ctx context.Context, url string, validators Validators) (Response, error)
}

// Response is one answer: its status, only the rate-related headers - never a
// whole header (watchpost D-83, I-1) - the validators for the next ask, and
// the body, empty on a 304.
type Response struct {
	Status     int
	Rate       RateHeaders
	Validators Validators
	Body       []byte
}

// RateHeaders are an answer's rate-related headers, as sent.
type RateHeaders struct{ RetryAfter, Limit, Remaining, Reset string }

// Validators let a host ask again for an answer only if it has changed.
type Validators struct{ ETag, LastModified string }

// Options are the library's settings. The reference circuit is fixed by
// ruling (watchpost D-73, D-91), so it is not an option; nor is the grid step,
// which is 2° (D-138).
type Options struct {
	Clock func() time.Time // the time now; time.Now when nil
}

// Source is one source the library reads or is built from: its name, the
// hosts it is asked on at run time (none for one used only at build time),
// its terms and the citation it asks for (R-4.1).
type Source = terms.Source

// Library makes snapshots through the host's fetcher.
type Library struct {
	fetch Fetcher
	clock func() time.Time
}

// errNoFetcher is New without the host's network.
var errNoFetcher = errors.New("ionomaps: New needs the host's Fetcher; the library opens no connection of its own")

// New is a library that asks through f. It fetches nothing until an update.
//
// Source: this library.
func New(f Fetcher, o Options) (*Library, error) {
	if f == nil {
		return nil, errNoFetcher
	}
	clock := o.Clock
	if clock == nil {
		clock = time.Now
	}
	return &Library{fetch: f, clock: clock}, nil
}

// Sources is every source the library reads or is built from, with its
// hosts, terms and citation: a host credits them, and allows only those hosts
// (R-4.1, watchpost D-113). Each call builds the list afresh, so it is the
// host's own copy.
//
// Source: this library; each entry's terms and citation as NOTICE gives them.
func (l *Library) Sources() []Source { return terms.All() }
